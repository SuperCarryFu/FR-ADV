import os

import cv2
from skimage.io import imsave
from skimage.io import imread
import numpy as np
import torch
import torch.nn.functional as F

def read_mimg():
    filePath = './uploads'
    pairs=os.listdir(filePath)
    for pair in pairs:
        if "source" in pair:
            src_pair="./uploads/"+pair
        else:
            tar_pair="./uploads/"+pair
    src_img = imread(src_pair).astype(np.float32)
    tar_img = imread(tar_pair).astype(np.float32)

    c=src_img.shape
    # d=c[0:2]
    # if d[0]!=112:
    #     src_img=cv2.resize(src_img,(112,112),interpolation=cv2.INTER_LINEAR)
    tar_img =cv2.resize(tar_img,(112,112),interpolation=cv2.INTER_LINEAR)
    src_img = torch.Tensor(src_img.transpose((2, 0, 1))[None, :]).to('cuda')
    tar_img = torch.Tensor(tar_img.transpose((2, 0, 1))[None, :]).to('cuda')
    # return src_img,tar_img,d
    return src_img,tar_img

def read_img(model,size):
    filePath = './uploads'
    pairs=os.listdir(filePath)
    for pair in pairs:
        if "source" in pair:
            src_pair="./uploads/"+pair
        else:
            tar_pair="./uploads/"+pair
    src_img = imread(src_pair).astype(np.float32)
    tar_img = imread(tar_pair).astype(np.float32)

    # c=src_img.shape
    # d=c[0:2]
    # if d[0]!=112:
        # src_img=cv2.resize(src_img,(112,112),interpolation=cv2.INTER_LINEAR)
    tar_img =cv2.resize(tar_img,size,interpolation=cv2.INTER_LINEAR)
    src_img = torch.Tensor(src_img.transpose((2, 0, 1))[None, :]).to('cuda')
    tar_img = torch.Tensor(tar_img.transpose((2, 0, 1))[None, :]).to('cuda')
    feat = model.forward(tar_img).detach().requires_grad_(False)
    # return src_img,tar_img,feat,d
    return src_img,tar_img,feat,size

def save_images(image,filename, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image = np.clip(image, 0, 255).astype(np.uint8)
    imsave(os.path.join(output_dir, filename), image.astype(np.uint8))

def run(Attacker, src_img,tar_img,feat,d):
        x_adv = Attacker.attack(images=src_img, img_ft=feat,d=d)
        img = x_adv[0].detach().cpu().numpy().transpose((1, 2, 0))
        # if d[0] != 112:
        #     img = cv2.resize(img, d, interpolation=cv2.INTER_LINEAR)
        npy_path = os.path.join("temp", str(1) + '.npy')
        np.save(npy_path, img)
        save_images(img, str(1) + '.png', "temp")