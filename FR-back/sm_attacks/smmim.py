import math
import random
import torch
import numpy as np
from attacks.base import ConstrainedMethod
import torch.nn.functional as F

def rescaling_method( noise):
    sign = torch.sign(noise)
    affine = -torch.log((torch.abs(noise))) / torch.log(torch.tensor(2.0))
    max, a = torch.max(affine, dim=2, keepdim=True)
    max, c = torch.max(max, dim=3, keepdim=True)
    affine = torch.ceil(max - affine + 1e-9)
    weight = 2.0 * torch.log((affine / max) + 1)
    if(torch.any(torch.isnan(weight))):
        weight=torch.ones(sign.shape).cuda()
    return torch.mul(weight, sign)

class MetaMIM(ConstrainedMethod):
    def __init__(self, model, goal, distance_metric, eps, iters=20, mu=1.0):
        super(MetaMIM, self).__init__(model, goal, distance_metric,  eps)
        self.iters = iters
        self.mu = mu

    def batch_grad_m(self,x, img_ft, alpha,model):
        global_grad = 0
        for _ in range(12):
            x_neighbor = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor = torch.clamp(x_neighbor, min=0, max=255).detach().requires_grad_(True)
            ft=model.forward((F.interpolate(x_neighbor, size=(112,112), mode='bilinear')))
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor.grad
            model.zero_grad()
            x=x_neighbor
        return global_grad

    def batch_grad(self,x, img_ft, alpha,model):
        global_grad = 0
        for _ in range(6):
            x_neighbor1 = x + torch.randn_like(x) * alpha
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = torch.clamp(x_neighbor1, min=0, max=255).detach().requires_grad_(True)
            ft = model.forward(x_neighbor1)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor1.grad
            model.zero_grad()
            x_neighbor1 = x + torch.randn_like(x) * alpha
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = torch.clamp(x_neighbor1, min=0, max=255).detach().requires_grad_(True)
            ft = model.forward(x_neighbor1)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor1.grad
            model.zero_grad()
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = x + torch.randn_like(x) *alpha
            x_neighbor1 = torch.clamp(x_neighbor1, min=0, max=255).detach().requires_grad_(True)
            ft = model.forward(x_neighbor1)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor1.grad
            model.zero_grad()
            x_neighbor = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor = torch.clamp(x_neighbor, min=0, max=255).detach().requires_grad_(True)
            ft=model.forward(x_neighbor)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor.grad



            model.zero_grad()
            x=x_neighbor
        return global_grad

    def attack(self, src,dict, models,size=(112,112)):
        tmp = src.clone().detach().requires_grad_(True)
        g1 = torch.zeros_like(tmp)
        g2 = torch.zeros_like(tmp)
        tmp_cat = src.clone().detach().requires_grad_(True)
        tmp_finally = src.clone().detach().requires_grad_(True)
        l = len(models)
        if l % 2 == 0:
            m = math.ceil(l / 2) + 1
        else:
            m = math.ceil(l / 2)
        for _ in range(self.iters):
            train_index = random.sample(range(l), m)
            test_index = train_index.pop()

            for i in train_index:
                feature1=models[i].forward((F.interpolate(tmp, size=size, mode='bilinear')))
                feature2=models[i].forward(dict)

                if self.goal == 'impersonate':
                    loss= torch.mean((feature2 - feature1) ** 2)
                else:
                    loss= -torch.mean((feature2 - feature1) ** 2)

                loss.backward()
                grad =tmp.grad
                g1 = g1 * self.mu + grad
                models[i].zero_grad()

                if self.distance_metric == 'linf':
                    tmp1 = tmp.clone().detach().requires_grad_(True)
                    ft1 = feature2.clone().detach().requires_grad_(True)
                    global_grad = self.batch_grad(tmp1, ft1, self.eps * 1.5, models[i])
                    noise = (global_grad + 1.0 * g1) / (1.0 * (24 + 1.0))
                    noise = noise / torch.mean(torch.abs(noise), dim=(1, 2, 3), keepdim=True)
                    tmp = tmp - 1.5 * self.eps / self.iters * rescaling_method(noise)
                else:
                    gg1 = g1 / g1.abs().mean(dim=[1, 2, 3], keepdim=True)
                    batch_size = gg1.size(0)
                    grad_2d = gg1.contiguous().view(batch_size, -1)
                    grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).contiguous().view(batch_size, 1, 1, 1)
                    grad_unit = gg1 / grad_norm
                    alpha = 1.5 * self.eps / self.iters * np.sqrt(gg1[0].numel())
                    tmp = tmp - alpha * grad_unit
                tmp = tmp.detach().requires_grad_(True)

            model=models[test_index]
            feature1 = model.forward((F.interpolate(tmp, size=size, mode='bilinear')))
            feature2 = model.forward(dict)
            if self.goal == 'impersonate':
                loss = torch.mean((feature2 - feature1) ** 2)
            else:
                loss = -torch.mean((feature2 - feature1) ** 2)
            loss.backward()
            grad = tmp.grad
            g2 = g2 * self.mu + grad
            model.zero_grad()

            if self.distance_metric == 'linf':
                tmp2 = tmp.clone().detach().requires_grad_(True)
                ft2 = feature2.clone().detach().requires_grad_(True)
                global_grad = self.batch_grad(tmp2, ft2, self.eps * 1.5, model)
                noise = (global_grad + 1.0 * g2) / (1.0 * (24 + 1.0))
                noise = noise / torch.mean(torch.abs(noise), dim=(1, 2, 3), keepdim=True)
                tmp_adv = tmp - 1.5 * self.eps / self.iters * rescaling_method(noise)
            else:
                gg2 = g2 / g2.abs().mean(dim=[1, 2, 3], keepdim=True)
                batch_size = gg2.size(0)
                grad_2d = gg2.contiguous().view(batch_size, -1)
                grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).contiguous().view(batch_size, 1, 1, 1)
                grad_unit = gg2 / grad_norm
                alpha = 1.5 * self.eps / self.iters * np.sqrt(gg2[0].numel())
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
                # delta_norm = torch.clamp(torch.norm(delta_2d, dim=1), min=r).view(batch_size, 1, 1, 1)
                delta_norm = torch.norm(delta_2d, dim=1).contiguous().view(batch_size, 1, 1, 1)

            factor = r / delta_norm

            tmp_finally = torch.clamp(tmp_cat + delta * factor, min=0, max=255)
            tmp_finally = torch.clamp(tmp_finally, min=0, max=255)

        return tmp_finally


