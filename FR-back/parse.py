from flask import request
from attacks.CIM import CIM
from attacks.DIM import DIM
from attacks.FGSM import FGSM
from attacks.MIM import MIM
from attacks.PGD import PGD
from attacks.TIM import TIM
from myutils.utils import read_img, run
from networks.get_model import getmodel


def parse_s ():
    eps = request.args.get("eps")
    eps=float(eps)
    goal = request.args.get("goal")
    if goal=="0":
        goal='impersonate'
    else:
        goal = 'dodging'
    metric = request.args.get("metric")
    if metric=="0":
        metric='l2'
    else:
        metric='linf'
    model = request.args.get("model")
    size = (112, 112)
    if model=="ShuffleNet_V2":
        model="ShuffleNet_V2_GDConv-stride1"
    if model == "ShuffleNet_V1":
        model="ShuffleNet_V1_GDConv"
    if model=="CosFace":
        size=(112,96)
    if model=="SphereFace":
        size=(112,96)
    if model=="FaceNet":
        model = "FaceNet-casia"
        size=(160,160)
    model, _ = getmodel(model, device='cuda')
    src_img, tar_img,tar_feat,d = read_img(model,size)

    attack = request.args.get("attack")
    if attack=="FGSM":
        attack = FGSM(model=model, goal=goal, eps=eps, distance_metric=metric)
        run(attack,src_img,tar_img,tar_feat,d)
    if attack=="PGD":
        iters = request.args.get("iters")
        iters = int(iters)
        attack = PGD(model=model, goal=goal, eps=eps, distance_metric=metric,iters=iters)
        run(attack,src_img,tar_img,tar_feat,d)
    if attack=="MIM":
        iters = request.args.get("iters")
        iters = int(iters)
        mu = request.args.get("mu")
        mu = float(mu)
        attack = MIM(model=model, goal=goal, eps=eps, distance_metric=metric,iters=iters,mu=mu)
        run(attack,src_img,tar_img,tar_feat,d)
    if attack=="CIM":
        iters = request.args.get("iters")
        iters = int(iters)
        length = request.args.get("length")
        length=int(length)
        attack = CIM(model=model, goal=goal, eps=eps, distance_metric=metric,iters=iters,length=length)
        run(attack,src_img,tar_img,tar_feat,d)
    if attack=="DIM":
        iters = request.args.get("iters")
        iters = int(iters)
        attack = DIM(model=model, goal=goal, eps=eps, distance_metric=metric,iters=iters)
        run(attack,src_img,tar_img,tar_feat,d)
    if attack=="TIM":
        iters = request.args.get("iters")
        iters = int(iters)
        kernel_len = request.args.get("kernel_len")
        kernel_len = int(kernel_len)
        nsig = request.args.get("nsig")
        nsig = int(nsig)
        attack = TIM(model=model, goal=goal, eps=eps, distance_metric=metric,iters=iters,kernel_len=kernel_len,nsig=nsig)
        run(attack,src_img,tar_img,tar_feat,d)
