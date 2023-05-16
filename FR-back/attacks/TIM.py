from attacks.base import ConstrainedMethod
import torch
import numpy as np
import torch.nn.functional as F

def smooth(stack_kernel, x):
    padding = (stack_kernel.size(-1) - 1) // 2
    groups = x.size(1)
    return F.conv2d(x, stack_kernel, padding=padding, groups=groups)

def gkern(kernlen=21, nsig=3):
    import scipy.stats as st
    x = np.linspace(-nsig, nsig, kernlen)
    kern1d = st.norm.pdf(x)
    kernel_raw = np.outer(kern1d, kern1d)
    kernel = kernel_raw / kernel_raw.sum()
    return kernel

class TIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps,kernel_len=7, nsig=3, iters=20, mu=1.0):
        super(TIM, self).__init__(model, goal, distance_metric, eps)
        self.iters = iters
        self.mu = mu
        kernel = gkern(kernel_len, nsig).astype(np.float32)
        stack_kernel = np.stack([kernel, kernel, kernel]).swapaxes(2, 0)
        stack_kernel = np.expand_dims(stack_kernel, 3)
        stack_kernel = stack_kernel.transpose((2, 3, 0, 1))
        self.stack_kernel = torch.from_numpy(stack_kernel).cuda()

    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach().requires_grad_(True)
        g = torch.zeros_like(images_adv)
        for _ in range(self.iters):
            features = self.model.forward((F.interpolate(images_adv, size=d, mode='bilinear')))
            loss = self.getLoss(features, img_ft)
            loss.backward()
            grad = smooth(self.stack_kernel, images_adv.grad)
            grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
            g = g * self.mu + grad
            self.model.zero_grad()
            images_adv = self.step(images_adv, 1.5 * self.eps / self.iters, g, images, self.eps)
            images_adv = images_adv.detach().requires_grad_(True)
        return images_adv

