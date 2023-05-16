# -*- coding: utf-8 -*-
import io
import os
import uuid
from urllib.parse import urljoin
from PIL import Image
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models

from Adv_GAN_1 import Adv_GAN
# from Adv_GAN import Adv_GAN
from base64_tr import img_str, img_str1
from parse import parse_s
from sm_a import todo

app = Flask(__name__)
CORS(app, supports_credentials=True,resources=r'/*')
######################
# 配置文件
######################
UPLOAD_FOLDER = 'uploads'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许的扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# 1M
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# 检查后缀名是否为允许的文件
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 获取文件名
def get_filename1(filename):
    ext = os.path.splitext(filename)[-1]
    uuidOne = uuid.uuid4()
    prefix="gan"
    return prefix+"_"+str(uuidOne) + ext

def get_filename(filename,src):
    ext = os.path.splitext(filename)[-1]
    uuidOne = uuid.uuid4()
    if src=="0":
        prefix="source"
    else:
        prefix="target"
    return prefix+"_"+str(uuidOne) + ext
# 上传文件
@app.route("/upload", methods=['POST'])
def upload():
    filePath = './uploads'
    pairs = os.listdir(filePath)
    src = request.args.get("src")
    src_pair=""
    tar_pair= ""
    if src == "0":
        for pair in pairs:
            if "source" in pair:
                src_pair = "./uploads/" + pair
                break
        if src_pair!="":
            os.remove(src_pair)
    else:
        for pair in pairs:
            if "target" in pair:
                tar_pair = "./uploads/" + pair
                break
        if tar_pair!="":
            os.remove(tar_pair)
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        print(file.filename)
        filename = get_filename(file.filename,src)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(os.path.join(app.root_path, filepath))
        file_url = urljoin(request.host_url, filepath)
        return file_url
    return "not allow ext"

@app.route("/uploadGAN", methods=['POST'])
def uploadGAN():
    filePath = './uploadsGAN'
    pairs = os.listdir(filePath)
    src_pair=''
    for pair in pairs:
        if "gan" in pair:
            src_pair = "./uploadsGAN/" + pair
            break
    if src_pair != "":
        os.remove(src_pair)
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        print(file.filename)
        filename = get_filename1(file.filename)
        filepath = os.path.join(filePath, filename)
        file.save(os.path.join(app.root_path, filepath))
        file_url = urljoin(request.host_url, filepath)
        return file_url
    return "not allow ext"
# 获取文件
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/uploadsGAN/<path:filename>')
def get_file1(filename):
    return send_from_directory('./uploadsGAN', filename)

@app.route('/getPic',methods=['GET', 'POST'])
def findpic():
    gan = Adv_GAN()
    img_url = './log/adv.png'
    with open(img_url, 'rb') as f:
        a = f.read()
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr,format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(imgByteArr)
    return  imgByteArr

@app.route('/gettar',methods=['GET', 'POST'])
def findpictar():
    # Adv_GAN()
    attack = request.args.get("attack")
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
    with open(img_url, 'rb') as f:
        a = f.read()
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr,format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(imgByteArr)
    return  imgByteArr

@app.route('/delete_1')
def delete_1():
    filePath = './uploads'
    pairs = os.listdir(filePath)
    for pair in pairs:
        if "source" in pair:
            src_pair = "./uploads/" + pair
            break
    os.remove(src_pair)
    return{'img':""}

@app.route('/delete_2')
def delete_2():
    filePath = './uploads'
    pairs = os.listdir(filePath)
    for pair in pairs:
        if "target" in pair:
            tar_pair = "./uploads/" + pair
            break
    os.remove(tar_pair)
    return{'img':""}

@app.route('/contrast')
def contrast():
    c,a, b = img_str()
    try:
        cred = credential.Credential("AKIDGL9hyyh9KErDH4ZnlRqypPijUyA5j8G7", "bvznLdfspVv4wYtxlIYXFfpiKfjV0EBq")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

        req = models.CompareFaceRequest()
        params = {
            "ImageA": a,
            "ImageB": b
        }
        req.from_json_string(json.dumps(params))
        resp = client.CompareFace(req)

        req1 = models.CompareFaceRequest()
        params = {
            "ImageA": c,
            "ImageB": b
        }
        req1.from_json_string(json.dumps(params))

        resp1 = client.CompareFace(req1)

        score1 = round(resp.Score, 2)
        score2 = round(resp1.Score, 2)
        print(resp.to_json_string())
        print(resp1.to_json_string())
        # string = resp.to_json_string()
        dictionary = {"score1": score1, "score2": score2}
        jsonString = json.dumps(dictionary)
        print(jsonString)

    except TencentCloudSDKException as err:
        print(err)

    return jsonString

@app.route('/contrast1')
def contrast1():
    c,a, b = img_str1()
    try:
        cred = credential.Credential("", "")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

        req = models.CompareFaceRequest()
        params = {
            "ImageA": a,
            "ImageB": b
        }
        req.from_json_string(json.dumps(params))
        resp = client.CompareFace(req)

        req1 = models.CompareFaceRequest()
        params = {
            "ImageA": c,
            "ImageB": b
        }
        req1.from_json_string(json.dumps(params))

        resp1 = client.CompareFace(req1)

        score1 = round(resp.Score, 2)
        score2 = round(resp1.Score, 2)
        print(resp.to_json_string())
        print(resp1.to_json_string())
        # string = resp.to_json_string()
        dictionary = {"score1": score1, "score2": score2}
        jsonString = json.dumps(dictionary)
        print(jsonString)
    except TencentCloudSDKException as err:
        print(err)

    # return resp.to_json_string()
    return jsonString

@app.route('/getMeta',methods=['GET', 'POST'])
def findpMeta():
    todo()
    img_url = './temp/1.png'
    with open(img_url, 'rb') as f:
        a = f.read()
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr,format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(imgByteArr)
    return  imgByteArr
if __name__ == '__main__':
    app.run(debug=True)