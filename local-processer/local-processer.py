import base64
import requests
import time
import sys
import cv2
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../animegan2-pytorch'))
import test_withsam

url = 'http://127.0.0.1:5000/img'

oldImgRes = requests.get(url)

def send():
    with open('result/res.jpg', 'rb') as f:
        imgData = base64.b64encode(f.read())
    
    data = {
        'filename': 'res.jpg',
        'imgData': imgData
    }
    ret = requests.request('post', 'http://127.0.0.1:5000/returnimg', data=data)
    print(ret)

while True:
    try:
        res = requests.get(url)
    except:
        continue

    if res.content == b'empty':
        time.sleep(7)
        continue

    if res != oldImgRes:
        oldImgRes = res
        f = open('img/receive.npy', 'wb')
        # import pdb; pdb.set_trace()
        f.write(res.content)
        f.close()
        img_xy = np.load('img/receive.npy', allow_pickle=True)
        print('{}    {}',img_xy.item()['x'], img_xy.item()['y'])

        # cv2.imshow("lalala", img_xy.item()['img'])

        test_withsam.transfer_image(img_xy.item()['img'], img_xy.item()['x'], img_xy.item()['y'])

        send()
        # break
    time.sleep(7)
    # import pdb; pdb.set_trace()