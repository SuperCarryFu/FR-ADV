from attacks.base import ConstrainedMethod
import torch
import numpy as np
import torch.nn.functional as F
def Cutout(length, img_shape):
    h, w = img_shape
    mask = np.ones((h, w, 3), np.float32)
    y = np.random.randint(h)
    x = np.random.randint(w)

    y1 = np.clip(y - length // 2, 0, h)
    y2 = np.clip(y + length // 2, 0, h)
    x1 = np.clip(x - length // 2, 0, w)
    x2 = np.clip(x + length // 2, 0, w)

    mask[y1: y2, x1: x2, :] = 0.
    return mask[None, :]

class CIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps, iters=20, mu=1.0, length=8):
        super(CIM, self).__init__(model, goal,distance_metric,  eps)
        self.iters = iters
        self.mu = mu
        self.length = length
    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach().requires_grad_(True)
        g = torch.zeros_like(images_adv)
        for _ in range(self.iters):
            img_shape = images_adv.shape[2:]
            mask = Cutout(self.length, img_shape)
            mask = torch.Tensor(mask.transpose((0, 3, 1, 2))).cuda()

            features = self.model.forward((F.interpolate(images_adv* mask, size=d, mode='bilinear')) )
            loss = self.getLoss(features, img_ft)
            loss.backward()
            grad = images_adv.grad
            grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
            g = g * self.mu + grad
            self.model.zero_grad()
            images_adv=self.step(images_adv, 1.5 * self.eps / self.iters, g, images, self.eps)
            images_adv = images_adv.detach().requires_grad_(True)
        return images_adv