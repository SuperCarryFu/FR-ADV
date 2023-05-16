# encoding:utf-8
import os
import base64
from flask import Flask, request, send_from_directory
def img_str():
    # 二进制读取图片,再将图片转为 base64 类型的字符串
    with open('./temp/1.png', 'rb') as fin:   #第一个参数为图片全路径或相对路径
        adv_data = fin.read()
        base64_data_bytes = base64.b64encode(adv_data)
        adv_str= base64_data_bytes.decode()

    tar_pair=""
    filePath = './uploads'
    pairs = os.listdir(filePath)
    for pair in pairs:
        if "target" in pair:
            tar_pair = "./uploads/" + pair
        if "source" in pair:
            src_pair = "./uploads/" + pair

    with open(tar_pair, 'rb') as fin:   #第一个参数为图片全路径或相对路径
        tar_data = fin.read()
        base64_data_bytes = base64.b64encode(tar_data)
        tar_str= base64_data_bytes.decode()

    with open(src_pair, 'rb') as fin:   #第一个参数为图片全路径或相对路径
        src_data = fin.read()
        base64_data_bytes = base64.b64encode(src_data)
        src_str= base64_data_bytes.decode()

    return src_str, adv_str,tar_str

def img_str1():
    # 二进制读取图片,再将图片转为 base64 类型的字符串
    filePath = './uploadsGAN'
    pairs = os.listdir(filePath)
    src_pair = ''
    for pair in pairs:
        src_pair = "./uploadsGAN/" + pair
    with open(src_pair, 'rb') as fin:   #第一个参数为图片全路径或相对路径
        src_data = fin.read()
        base64_data_bytes = base64.b64encode(src_data)
        src_str= base64_data_bytes.decode()
    with open('./log/adv.png', 'rb') as fin:   #第一个参数为图片全路径或相对路径
        adv_data = fin.read()
        base64_data_bytes = base64.b64encode(adv_data)
        adv_str= base64_data_bytes.decode()
    attack = request.args.get("attack")
    # tar_pair=""
    if attack=="模型1":
        img_url = './traget/0b8f14c8-4117-4aab-b951-761159d642c5.jpg'
    if attack=="模型2":
        img_url = './traget/0c0df5d0-b706-4c6e-bd3d-ba6d0198ee50.jpg'
    if attack=="模型3":
        img_url = './traget/1b03e94f-22cd-4e10-8f57-dd691275e885.jpg'
    if attack=="模型4":
        img_url = './traget/1b8102cb-bc9e-4c2a-8a19-55e2c9e6d232.jpg'
    if attack=="模型5":
        img_url = './traget/1cef1274-7678-426a-ada5-addd58cd8077.jpg'
    if attack=="模型6":
        img_url = './traget/01c9848a-db70-45ad-a0f7-0944701c457e.jpg'
    if attack=="模型7":
        img_url = './traget/01f1ce7f-ce1f-43ae-8f12-d6e9ff7b1553.jpg'
    if attack=="模型8":
        img_url = './traget/2cbfb793-1699-4ba1-9d6b-b81da588d4ff.jpg'
    if attack=="模型9":
        img_url = './traget/2dc52960-c5d0-4ac6-aee8-994444fce03b.jpg'
    if attack=="模型10":
        img_url = './traget/2f47688c-6549-4840-9415-b6ae0b73e52f.jpg'
    # filePath = './uploads'
    # pairs = os.listdir(filePath)
    # for pair in pairs:
    #     if "target" in pair:
    #         tar_pair = "./uploads/" + pair
    #         break
    with open(img_url, 'rb') as fin:   #第一个参数为图片全路径或相对路径
        tar_data = fin.read()
        base64_data_bytes = base64.b64encode(tar_data)
        tar_str= base64_data_bytes.decode()

    return src_str,adv_str,tar_str