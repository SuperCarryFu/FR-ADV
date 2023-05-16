from attacks.base import ConstrainedMethod
import torch
import torch.nn.functional as F
class MIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps, iters=20, mu=1.0):
        super(MIM, self).__init__(model, goal, distance_metric, eps)
        self.iters = iters
        self.mu = mu
    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach().requires_grad_(True)
        g = torch.zeros_like(images_adv)
        for _ in range(self.iters):
            features = self.model.forward((F.interpolate(images_adv, size=d, mode='bilinear')))
            loss = self.getLoss(features, img_ft)
            loss.backward()
            grad = images_adv.grad
            grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
            g = g * self.mu + grad
            self.model.zero_grad()
            images_adv = self.step(images_adv, 1.5 * self.eps / self.iters, g, images, self.eps)
            images_adv = images_adv.detach().requires_grad_(True)
        return images_adv

