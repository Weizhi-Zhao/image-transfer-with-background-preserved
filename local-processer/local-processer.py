import base64
import requests
import time
import sys
import cv2
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../animegan2-pytorch'))
import test_withsam

# url = 'http://8.130.91.10:5000/img'
url = 'http://127.0.0.1:5000'

oldImgRes = requests.get(url)

def send():
    with open('result/res.jpg', 'rb') as f:
        imgData = base64.b64encode(f.read())
    
    data = {
        'filename': 'res.jpg',
        'imgData': imgData
    }
    ret = requests.request('post', url + '/returnimg', data=data)
    print(ret)

while True:
    try:
        res = requests.get(url + '/img')
        print('ok')
    except:
        continue

    if res.content == b'empty':
        time.sleep(7)
        continue

    if res != oldImgRes:
        oldImgRes = res
        with open('img/receive.npy', 'wb') as f:
            f.write(res.content)
        img_xy = np.load('img/receive.npy', allow_pickle=True)
        print('{}    {}',img_xy.item()['x'], img_xy.item()['y'])

        with open('img/receive.jpg', 'wb') as f:
            f.write(img_xy.item()['img'])
        img = cv2.imread('img/receive.jpg')

        test_withsam.transfer_image(img, img_xy.item()['x'], img_xy.item()['y'])

        send()
        # break
    time.sleep(7)
    # import pdb; pdb.set_trace()