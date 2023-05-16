import numpy as np
import torch
from attacks.base import ConstrainedMethod
import torch.nn.functional as F

class FGSM(ConstrainedMethod):
    def __init__(self, model,goal, distance_metric, eps=1.6):
        super(FGSM, self).__init__(model,goal, distance_metric, eps)

    def attack(self, images, img_ft,d):
        images_adv = images.clone().detach().requires_grad_(True)
        # features = self.model.forward(images_adv)
        features = self.model.forward((F.interpolate(images_adv, size=d, mode='bilinear')))
        loss = self.getLoss(features, img_ft)
        loss.backward()
        grad = images_adv.grad
        self.model.zero_grad()
        images_adv = self.step(images_adv, self.eps, grad, images, self.eps)


        return images_adv
