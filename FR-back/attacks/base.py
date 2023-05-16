import torch
import numpy as np
class Attack(object):
    def __init__(self, model, goal, distance_metric):
        assert(goal == 'dodging' or goal == 'impersonate')
        assert (distance_metric == 'linf' or distance_metric == 'l2')
        self.model = model
        self.goal = goal
        self.distance_metric = distance_metric

class ConstrainedMethod(Attack):
    def __init__(self, model, goal,distance_metric,  eps):
        super(ConstrainedMethod, self).__init__(model, goal,distance_metric)
        self.eps = eps

    def rescaling_method(self,noise):
        sign = torch.sign(noise)
        affine = -torch.log((torch.abs(noise)))/torch.log(torch.tensor(2.0))

        max,a = torch.max(affine, dim=2,keepdim=True)
        max,c = torch.max(max, dim=3, keepdim=True)
        affine = torch.ceil(max - affine + 1e-9)

        weight=2.0*torch.log((affine/max)+1)
        if(torch.any(torch.isnan(weight))):
            weight=torch.ones(sign.shape).cuda()
        return torch.mul(weight, sign)

    def getLoss(self, features, ys):
        if self.goal == 'impersonate':
            return torch.mean((ys - features) ** 2)
        else:
            return -torch.mean((ys - features) ** 2)

    def clip_by_value(self, xs_adv, xs, eps):
        minx = torch.clamp(xs - eps, min=0)
        maxx = torch.clamp(xs + eps, max=255)
        xs_adv = torch.min(xs_adv, maxx)
        xs_adv = torch.max(xs_adv, minx)
        return xs_adv

    def clip_by_norm(self, xs_adv, xs, r):
        delta = xs_adv - xs
        batch_size = delta.size(0)
        delta_2d = delta.contiguous().view(batch_size, -1)
        if isinstance(r, torch.Tensor):
            delta_norm = torch.max(torch.norm(delta_2d, dim=1), r.contiguous().view(-1)).contiguous().view(batch_size, 1, 1, 1)
        else:
            delta_norm = torch.clamp(torch.norm(delta_2d, dim=1), min=r).contiguous().view(batch_size, 1, 1, 1)
        factor = r / delta_norm
        return xs + delta * factor

    def step(self, xs_adv, lr, grad, xs, eps):
        if self.distance_metric == 'linf':
            xs_adv = xs_adv - lr * torch.sign(grad)
            xs_adv = self.clip_by_value(xs_adv, xs, eps)
        else:
            batch_size = grad.size(0)
            grad_2d = grad.contiguous().view(batch_size, -1)
            grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).contiguous().view(batch_size, 1, 1, 1)
            grad_unit = grad / grad_norm
            alpha = lr * np.sqrt(grad[0].numel())
            xs_adv = xs_adv - alpha * grad_unit
            xs_adv = self.clip_by_norm(xs_adv, xs, eps * np.sqrt(grad[0].numel()))
        return torch.clamp(xs_adv, min=0, max=255)

    def batch_grad(self,x, img_ft, alpha):
        global_grad = 0
        for _ in range(12):
            x_neighbor = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor = torch.clamp(x_neighbor, min=0, max=255).detach().requires_grad_(True)
            ft=self.model.forward(x_neighbor)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor.grad
            self.model.zero_grad()
            x=x_neighbor
        return global_grad

    def step_s(self, xs_adv, lr, grad, xs, eps,images_adv,img_ft):
        if self.distance_metric == 'linf':
            global_grad = self.batch_grad(images_adv, img_ft, self.eps * 1.5)
            noise = (global_grad + 1.0 * grad) / (1.0 * (12 + 1.0))
            noise = noise / torch.mean(torch.abs(noise), dim=(1, 2, 3), keepdim=True)
            xs_adv = xs_adv - lr * self.rescaling_method(noise)
            xs_adv = self.clip_by_value(xs_adv, xs, eps)
        else:
            grad = grad / grad.abs().mean(dim=[1, 2, 3], keepdim=True)
            batch_size = grad.size(0)
            grad_2d = grad.view(batch_size, -1)
            grad_norm = torch.clamp(torch.norm(grad_2d, dim=1), min=1e-12).view(batch_size, 1, 1, 1)
            grad_unit = grad / grad_norm
            alpha = lr * np.sqrt(grad[0].numel())
            xs_adv = xs_adv - alpha * grad_unit
            xs_adv = self.clip_by_norm(xs_adv, xs, eps * np.sqrt(grad[0].numel()))
        return torch.clamp(xs_adv, min=0, max=255)
