import torch
from attacks.base import ConstrainedMethod
import random
import torch.nn.functional as F

def Resize_and_Padding(x, scale_factor):
    h, w = x.shape[-2:]
    resized_h, resized_w = round(h * scale_factor), round(w * scale_factor)
    new_x = torch.zeros_like(x)
    offset_h, offset_w = random.randint(0, h - resized_h), random.randint(0, w - resized_w)
    new_x[:, :, offset_h:offset_h + resized_h, offset_w:offset_w + resized_w] = F.interpolate(x, (resized_h, resized_w))
    return new_x

class DIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric,eps=8,iters=20, mu=1.0):
        super(DIM, self).__init__(model, goal, distance_metric, eps)
        self.iters = iters
        self.mu = mu

    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach().requires_grad_(True)
        g = torch.zeros_like(images_adv)
        for _ in range(self.iters):
            scale_factor = random.uniform(0.9, 1)
            features = self.model.forward(Resize_and_Padding((F.interpolate(images_adv, size=d, mode='bilinear')), scale_factor))
            loss = self.getLoss(features, img_ft)
            loss.backward()
            grad = images_adv.grad
            grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
            g = g * self.mu + grad
            self.model.zero_grad()
            images_adv=self.step(images_adv, 1.5 * self.eps / self.iters, g, images, self.eps)
            images_adv = images_adv.detach().requires_grad_(True)
        return images_adv