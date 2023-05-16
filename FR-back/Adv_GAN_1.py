from flask import request
from PIL import Image
from torchvision import transforms
from generator import SSAE
from torchvision.utils import save_image
import onnxruntime as onx
import torch.onnx
import os
from skimage.io import imread, imsave
import numpy as np
import torch

def read_img(data_dir):
    src = Image.open(data_dir)
    transform = transforms.Compose([
        transforms.ToTensor(),
        ])
    img=transform(src)
    img=torch.unsqueeze(img, dim=0)
    # img=img*255
    return img
def clamp(input, min=None, max=None):
    if min is not None and max is not None:
        return torch.clamp(input, min=min, max=max)
    elif min is None and max is None:
        return input
    elif min is None and max is not None:
        return torch.clamp(input, max=max)
    elif min is not None and max is None:
        return torch.clamp(input, min=min)
    else:
        raise ValueError("This is impossible")
def _batch_clamp_tensor_by_vector(vector, batch_tensor):
    return torch.min(
        torch.max(batch_tensor.transpose(0, -1), -vector), vector
    ).transpose(0, -1).contiguous()
def batch_clamp(float_or_vector, tensor):
    if isinstance(float_or_vector, torch.Tensor):
        assert len(float_or_vector) == len(tensor)
        tensor = _batch_clamp_tensor_by_vector(float_or_vector, tensor)
        return tensor
    elif isinstance(float_or_vector, float):
        tensor = clamp(tensor, -float_or_vector, float_or_vector)
    else:
        raise TypeError("Value has to be float or torch.Tensor")
    return tensor
def save_images(image, filename, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image = np.clip(image, 0, 255).astype(np.uint8)
    imsave(os.path.join(output_dir, filename), image.astype(np.uint8))
def read_pair(path):
    img = imread(path).astype(np.float32)
    img = torch.Tensor(img.transpose((2, 0, 1))[None, :])
    return img
def Adv_GAN ():
    generator = SSAE().to('cuda')
    attack = request.args.get("attack")
    if attack == "模型1":
        sess = onx.InferenceSession("./checkpoint/33.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型2":
        img_url = './traget/0c0df5d0-b706-4c6e-bd3d-ba6d0198ee50.jpg'
        sess = onx.InferenceSession("./checkpoint/ckpt_best_2_opt.onnx", providers=['CUDAExecutionProvider'])

    if attack=="模型3":
        img_url = './traget/1b03e94f-22cd-4e10-8f57-dd691275e885.jpg'
        sess = onx.InferenceSession("./checkpoint/3.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型4":
        img_url = './traget/1b8102cb-bc9e-4c2a-8a19-55e2c9e6d232.jpg'
        sess = onx.InferenceSession("./checkpoint/4.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型5":
        img_url = './traget/1cef1274-7678-426a-ada5-addd58cd8077.jpg'
        sess = onx.InferenceSession("./checkpoint/5.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型6":
        img_url = './traget/01c9848a-db70-45ad-a0f7-0944701c457e.jpg'
        sess = onx.InferenceSession("./checkpoint/6.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型7":
        img_url = './traget/01f1ce7f-ce1f-43ae-8f12-d6e9ff7b1553.jpg'
        sess = onx.InferenceSession("./checkpoint/7.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型8":
        img_url = './traget/2cbfb793-1699-4ba1-9d6b-b81da588d4ff.jpg'
        sess = onx.InferenceSession("./checkpoint/8.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型9":
        img_url = './traget/2dc52960-c5d0-4ac6-aee8-994444fce03b.jpg'
        sess = onx.InferenceSession("./checkpoint/9.opt.onnx", providers=['CUDAExecutionProvider'])
    if attack=="模型10":
        img_url = './traget/2f47688c-6549-4840-9415-b6ae0b73e52f.jpg'
        sess = onx.InferenceSession("./checkpoint/10.opt.onnx", providers=['CUDAExecutionProvider'])
    if generator:
        generator.eval()
    filePath = './uploadsGAN'
    pairs = os.listdir(filePath)
    for pair in pairs:
        c='./uploadsGAN/'+pair

    img = read_img(c)
    img1 = img.numpy()
    input_name = sess.get_inputs()[0].name
    out_name0 = sess.get_outputs()[0].name
    out_name1 = sess.get_outputs()[1].name
    results = sess.run([out_name0, out_name1], {input_name: img1})  # infe
    perturbations = torch.from_numpy(results[0])
    saliency_map = torch.from_numpy(results[1])
    perturbations_with_saliency = perturbations * saliency_map * 255
    src = img * 255
    adv = src + perturbations_with_saliency

    minx = torch.clamp(src - 8.0, min=0)
    maxx = torch.clamp(src + 8.0, max=255)
    adv = torch.min(adv, maxx)
    adv = torch.max(adv, minx)
    # save_images(adv[0].detach().cpu().numpy().transpose((1, 2, 0)), 'adv.png', './log/')
    save_image(adv, './log/adv.png', normalize=True)

    pair1 = read_pair('./log/adv.png')
    pair2 = read_pair(c)
    minx = torch.clamp(pair2 - 8, min=0)
    maxx = torch.clamp(pair2 + 8, max=255)
    pair1 = torch.min(pair1, maxx)
    pair1 = torch.max(pair1, minx)
    img = pair1[0].numpy().transpose((1, 2, 0))
    save_images(img, 'adv.png', './log/')

    print("cc")