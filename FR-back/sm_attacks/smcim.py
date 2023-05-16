import math
import random
import torch
import numpy as np
from attacks.base import ConstrainedMethod

def rescaling_method(noise):
    sign = torch.sign(noise)
    affine = -torch.log((torch.abs(noise))) / torch.log(torch.tensor(2.0))
    max, a = torch.max(affine, dim=2, keepdim=True)
    max, c = torch.max(max, dim=3, keepdim=True)
    affine = torch.ceil(max - affine + 1e-9)
    weight = 2.0 * torch.log((affine / max) + 1)
    if (torch.any(torch.isnan(weight))):
        weight = torch.ones(sign.shape).cuda()
    return torch.mul(weight, sign)

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

class MetaCIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps, iters=20, length=8):
        super(MetaCIM, self).__init__(model, goal, distance_metric, eps)
        self.iters = iters
        self.length = length

    def batch_grad_m(self,x, img_ft, alpha,model):
        global_grad = 0
        for _ in range(12):
            x_neighbor = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor = torch.clamp(x_neighbor, min=0, max=255).detach().requires_grad_(True)
            ft=model.forward(x_neighbor)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor.grad
            model.zero_grad()
            x=x_neighbor
        return global_grad

    def attack(self, src, dict, models):
        tmp = src.clone().detach().requires_grad_(True)
        tmp_cat = src.clone().detach().requires_grad_(True)
        tmp_finally = src.clone().detach().requires_grad_(True)
        l = len(models)
        if l % 2 == 0:
            m = math.ceil(l / 2) + 1
        else:
            m = math.ceil(l / 2)
        for _ in range(self.iters):
            img_shape = tmp.shape[2:]
            mask = Cutout(self.length, img_shape)
            mask = torch.Tensor(mask.transpose((0, 3, 1, 2))).cuda()
            train_index = random.sample(range(l), m)
            test_index = train_index.pop()
            for i in train_index:
                feature1 = models[i].forward(tmp * mask)
                feature2 = models[i].forward(dict)

                if self.goal == 'impersonate':
                    loss = torch.mean((feature2 - feature1) ** 2)
                else:
                    loss = -torch.mean((feature2 - feature1) ** 2)
                loss.backward()
                grad = tmp.grad
                models[i].zero_grad()
                if self.distance_metric == 'linf':
                    tmp1 = tmp.clone().detach().requires_grad_(True)
                    ft1 = feature2.clone().detach().requires_grad_(True)
                    global_grad = self.batch_grad_m(tmp1, ft1, self.eps * 1.5, models[i])
                    noise = (global_grad + 1.0 * grad) / (1.0 * (12 + 1.0))
                    noise = noise / torch.mean(torch.abs(noise), dim=(1, 2, 3), keepdim=True)
                    tmp = tmp - 1.5 * self.eps / self.iters * rescaling_method(noise)
                else:
                    grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
                    batch_size = grad.size(0)
                    grad_2d = grad.contiguous().view(batch_size, -1)
                    grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).contiguous().view(batch_size, 1, 1, 1)
                    grad_unit = grad / grad_norm
                    alpha = 1.5 * self.eps / self.iters * np.sqrt(grad[0].numel())
                    tmp = tmp - alpha * grad_unit
                tmp = tmp.detach().requires_grad_(True)

            model = models[test_index]
            feature1 = model.forward(tmp * mask)
            feature2 = model.forward(dict)
            if self.goal == 'impersonate':
                loss = torch.mean((feature2 - feature1) ** 2)
            else:
                loss = -torch.mean((feature2 - feature1) ** 2)
            loss.backward()
            grad = tmp.grad
            model.zero_grad()

            if self.distance_metric == 'linf':
                tmp2 = tmp.clone().detach().requires_grad_(True)
                ft2 = feature2.clone().detach().requires_grad_(True)
                global_grad = self.batch_grad_m(tmp2, ft2, self.eps * 1.5, model)
                noise = (global_grad + 1.0 * grad) / (1.0 * (12 + 1.0))
                noise = noise / torch.mean(torch.abs(noise), dim=(1, 2, 3), keepdim=True)
                tmp_adv = tmp - 1.5 * self.eps / self.iters * rescaling_method(noise)
            else:
                grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
                batch_size = grad.size(0)
                grad_2d = grad.contiguous().view(batch_size, -1)
                grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).contiguous().view(batch_size, 1, 1, 1)
                grad_unit = grad / grad_norm
                alpha = 1.5 * self.eps / self.iters * np.sqrt(grad[0].numel())
                tmp_adv = tmp - alpha * grad_unit

            perturbation = tmp_adv - tmp
            tmp = tmp_finally + perturbation
            tmp_finally = tmp
            tmp = tmp.detach().requires_grad_(True)

        if self.distance_metric == 'linf':
            minx = torch.clamp(tmp_cat - self.eps, min=0)
            maxx = torch.clamp(tmp_cat + self.eps, max=255)
            tmp_finally = torch.min(tmp_finally, maxx)
            tmp_finally = torch.max(tmp_finally, minx)
        else:
            delta = tmp_finally - tmp_cat
            batch_size = delta.size(0)
            r = self.eps * np.sqrt(delta[0].numel())
            delta_2d = delta.contiguous().view(batch_size, -1)
            if isinstance(r, torch.Tensor):
                delta_norm = torch.max(torch.norm(delta_2d, dim=1), r.contiguous().view(-1)).contiguous().view(batch_size, 1, 1, 1)
            else:
                delta_norm = torch.norm(delta_2d, dim=1).contiguous().view(batch_size, 1, 1, 1)
            factor = r / delta_norm
            tmp_finally = torch.clamp(tmp_cat + delta * factor, min=0, max=255)
            tmp_finally = torch.clamp(tmp_finally, min=0, max=255)
        return tmp_finally
