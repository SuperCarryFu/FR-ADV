import os
import numpy as np
from flask import request
import cv2
from myutils.utils import save_images, read_mimg
from networks.get_model import getmodel
from sm_attacks.smcim import MetaCIM
from sm_attacks.smdim import MetaDIM
from sm_attacks.smmim import MetaMIM
from sm_attacks.smpgd import MetaPGD
from sm_attacks.smtim import MetaTIM

def todo():
    eps = request.args.get("eps")
    eps = float(eps)
    goal = request.args.get("goal")
    if goal == "0":
        goal = 'impersonate'
    else:
        goal = 'dodging'
    metric = request.args.get("metric")
    if metric == "0":
        metric = 'l2'
    else:
        metric = 'linf'
    models = request.args.get("models")
    model_s = []

    if models=="All":
        model, _ = getmodel("ShuffleNet_V2_GDConv-stride1", device='cuda')
        model_s.append(model)
        model, _ = getmodel("ShuffleNet_V1_GDConv", device='cuda')
        model_s.append(model)
        model, _ = getmodel("MobileFace", device='cuda')
        model_s.append(model)
        model, _ = getmodel("ArcFace", device='cuda')
        model_s.append(model)
        model, _ = getmodel("MobilenetV2", device='cuda')
        model_s.append(model)
        model, _ = getmodel("IR50-Softmax", device='cuda')
        model_s.append(model)
        model, _ = getmodel("IR50-CosFace", device='cuda')
        model_s.append(model)
        model, _ = getmodel("IR50-Am", device='cuda')
        model_s.append(model)
        model, _ = getmodel("Mobilenet-stride1", device='cuda')
        model_s.append(model)
        model, _ = getmodel("IR50-SphereFace", device='cuda')
        model_s.append(model)
    else:
        metas = models.split(",")
        for index, model in enumerate(metas):
            if model == "ShuffleNet_V2":
                model = "ShuffleNet_V2_GDConv-stride1"
            if model == "ShuffleNet_V1":
                model = "ShuffleNet_V1_GDConv"
            if model=="Mobilenet":
                model="Mobilenet-stride1"
            model, _ = getmodel(model, device='cuda')
            model_s.append(model)
    src_img, tar_img = read_mimg()

    attack = request.args.get("attack")
    # if attack == "FGSM":
    #     attack = FGSM(model=model, goal=goal, eps=eps, distance_metric=metric)
    #     run(attack, src_img, tar_img, tar_feat, d)
    if attack == "改进PGD":
        iters = request.args.get("iters")
        iters = int(iters)
        attack = MetaPGD(model=None, goal=goal, eps=eps, distance_metric=metric, iters=iters)
        x_adv = attack.attack(src=src_img, dict=tar_img,models=model_s)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")
    if attack == "改进MIM":
        iters = request.args.get("iters")
        iters = int(iters)
        mu = request.args.get("mu")
        mu = float(mu)
        attack = MetaMIM(model=None, goal=goal, eps=eps, distance_metric=metric, iters=iters, mu=mu)
        x_adv = attack.attack(src=src_img, dict=tar_img, models=model_s)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")
    if attack == "改进CIM":
        iters = request.args.get("iters")
        iters = int(iters)
        length = request.args.get("length")
        length = int(length)
        attack = MetaCIM(model=None, goal=goal, eps=eps, distance_metric=metric, iters=iters, length=length)
        x_adv = attack.attack(src=src_img, dict=tar_img, models=model_s)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")
    if attack == "改进DIM":
        iters = request.args.get("iters")
        iters = int(iters)
        attack = MetaDIM(model=None, goal=goal, eps=eps, distance_metric=metric, iters=iters)
        x_adv = attack.attack(src=src_img, dict=tar_img, models=model_s)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")
    if attack == "改进TIM":
        iters = request.args.get("iters")
        iters = int(iters)
        kernel_len = request.args.get("kernel_len")
        kernel_len = int(kernel_len)
        nsig = request.args.get("nsig")
        nsig = int(nsig)
        attack = MetaTIM(model=None, goal=goal, eps=eps, distance_metric=metric, iters=iters, kernel_len=kernel_len,
                     nsig=nsig)
        x_adv = attack.attack(src=src_img, dict=tar_img, models=model_s)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")
