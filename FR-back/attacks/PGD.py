import torch
from attacks.base import ConstrainedMethod
import torch.nn.functional as F
class PGD(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps=8, iters=20):
        super(PGD, self).__init__(model, goal, distance_metric, eps)
        self.iters = iters
    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach()
        images_adv = images_adv + torch.empty_like(images_adv).uniform_(-self.eps, self.eps)
        images_adv = torch.clamp(images_adv, min=0, max=255).detach().requires_grad_(True)
        # images_adv.requires_grad = True
        for _ in range(self.iters):
            features = self.model.forward((F.interpolate(images_adv, size=d, mode='bilinear')))
            loss = self.getLoss(features, img_ft)
            loss.backward()
            grad = images_adv.grad
            self.model.zero_grad()
            images_adv=self.step(images_adv, 1.5 * self.eps / self.iters, grad, images, self.eps)
            images_adv = images_adv.detach().requires_grad_(True)
        return images_adv