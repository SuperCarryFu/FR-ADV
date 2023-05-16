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

class MetaTIM(ConstrainedMethod):
    def __init__(self, model,goal, distance_metric, eps=1.6,iters=20,mu=1,kernel_len=7,nsig=3):
        super(MetaTIM, self).__init__(model,goal, distance_metric, eps)
        self.iters = iters
        self.mu = mu
        kernel = gkern(kernel_len, nsig).astype(np.float32)
        stack_kernel = np.stack([kernel, kernel, kernel]).swapaxes(2, 0)
        stack_kernel = np.expand_dims(stack_kernel, 3)
        stack_kernel = stack_kernel.transpose((2, 3, 0, 1))
        self.stack_kernel = torch.from_numpy(stack_kernel).cuda()

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
        for _ in range(12):
            x_neighbor1 = x + torch.randn_like(x) * math.sqrt(alpha)
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = torch.clamp(x_neighbor1, min=0, max=255).detach().requires_grad_(True)
            ft = model.forward(x_neighbor1)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor1.grad
            model.zero_grad()
            x_neighbor1 = x + torch.randn_like(x) * math.sqrt(alpha)
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = torch.clamp(x_neighbor1, min=0, max=255).detach().requires_grad_(True)
            ft = model.forward(x_neighbor1)
            loss = self.getLoss(ft, img_ft)
            loss.backward()
            global_grad += x_neighbor1.grad
            model.zero_grad()
            # x_neighbor1 = x + torch.empty_like(x).uniform_(-alpha, alpha)
            x_neighbor1 = x + torch.randn_like(x) *math.sqrt(alpha)
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
        tmp_cat = src.clone().detach()
        tmp_finally = src.clone().detach()
        l = len(models)
        if l % 2 == 0:
            m = math.ceil(l / 2) + 1
        else:
            m = math.ceil(l / 2)
        # 攻击开始（迭代）
        for _ in range(self.iters):
            # 选取元训练模型和元测试模型
            train_index = random.sample(range(l), m)
            test_index = train_index.pop()

            # 元训练开始
            for i in train_index:
                feature1=models[i].forward((F.interpolate(tmp, size=size, mode='bilinear')))
                feature2=models[i].forward(dict)
                # 计算损失
                if self.goal == 'impersonate':
                    loss= torch.mean((feature2 - feature1) ** 2)
                else:
                    loss= -torch.mean((feature2 - feature1) ** 2)
                    # 反向传播得到梯度
                loss.backward()
                grad = tmp.grad
                models[i].zero_grad()
                grad = smooth(self.stack_kernel, grad)
                if self.distance_metric == 'linf':
                    tmp1 = tmp.clone().detach().requires_grad_(True)
                    ft1 = feature2.clone().detach().requires_grad_(True)
                    global_grad = self.batch_grad(tmp1, ft1, self.eps * 1.5, models[i])
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

            # 元测试
            model=models[test_index]
            feature1 = model.forward((F.interpolate(tmp, size=size, mode='bilinear')))
            feature2 = model.forward(dict)
            if self.goal == 'impersonate':
                loss = torch.mean((feature2 - feature1) ** 2)
            else:
                loss = -torch.mean((feature2 - feature1) ** 2)

            loss.backward()
            grad = tmp.grad
            model.zero_grad()
            grad = smooth(self.stack_kernel, grad)
            if self.distance_metric == 'linf':
                tmp2 = tmp.clone().detach().requires_grad_(True)
                ft2 = feature2.clone().detach().requires_grad_(True)
                global_grad = self.batch_grad(tmp2, ft2, self.eps * 1.5, model)
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


            perturbation=tmp_adv-tmp
            tmp=tmp_finally+perturbation
            tmp_finally=tmp
            tmp = tmp.detach().requires_grad_(True)

        if self.distance_metric == 'linf':
            minx = torch.clamp(tmp_cat - self.eps, min=0)
            maxx = torch.clamp(tmp_cat + self.eps, max=255)
            tmp_finally = torch.min(tmp_finally, maxx)
            tmp_finally = torch.max(tmp_finally, minx)
        else:
            delta = tmp_finally - tmp_cat
            batch_size = delta.size(0)
            r=self.eps * np.sqrt(delta[0].numel())
            delta_2d = delta.contiguous().view(batch_size, -1)
            if isinstance(r, torch.Tensor):
                delta_norm = torch.max(torch.norm(delta_2d, dim=1), r.contiguous().view(-1)).contiguous().view(batch_size, 1, 1, 1)
            else:
                delta_norm = torch.norm(delta_2d, dim=1).contiguous().view(batch_size, 1, 1, 1)

            factor = r / delta_norm

            tmp_finally = torch.clamp(tmp_cat + delta * factor, min=0,max=255)
            tmp_finally = torch.clamp(tmp_finally, min=0, max=255)

        return tmp_finally


