import base64
from flask import Flask, request, redirect, render_template, url_for, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask import send_from_directory
# from gevent import pywsgi
import os
import cv2
import sys
import numpy as np
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../animegan2-pytorch'))
import test_withsam

app = Flask(__name__)

app.config['UPLOADED_PHOTO_DEST'] = os.path.join(os.getcwd(), 'photos')  # 当前工作目录
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
app.static_folder = 'static'

photos = UploadSet('PHOTO', IMAGES)  # 大概是给上传的文件分类，然后限制上传文件类型
configure_uploads(app, photos)  # 大概是初始化一下
haveSent = False

@app.route('/', methods=['POST', 'GET'])
def UL():
    del_files('photos')
    # TODO 这段程序具体还没搞懂
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])  # 好像'photo'就是上传的文件名
        return redirect(url_for('mouse', name=filename))
    return render_template('UL.html')

@app.route('/photo/<name>')
def mouse(name):
    if name is None:
        abort(404)
    url = photos.url(name)
    selfUrl = request.url
    return render_template('mouse.html', url=url, name=name, selfUrl=selfUrl)


@app.route('/result/<name>/<x>/<y>/<ex>/<ey>')
def showEffRes(name, x, y, ex, ey):
    global haveSent
    if name is None:
        abort(404)
    url = photos.url(name)  # 对photos这个set调用.url()方法，即可获取文件（具体的不懂）
    img = cv2.imread(os.path.join('photos', name), cv2.IMREAD_COLOR)
    height, width, _ = img.shape
    x = eval(x)
    y = eval(y)
    ex = eval(ex)
    ey = eval(ey)
    y = (y - ey) / 350 * height
    x = (x - ex) / 350 * height
    if x > width or x < 0 or y > height or y < 0:
        return redirect(url_for('mouse', name=name))
    print("选点成功")
    img_xy_dict = {
        'x': x,
        'y': y,
        'img': img
    }
    try:    
        os.remove('static/images/res.jpg')
    except:
        pass
    haveSent = False
    np.save('zwz_sending/send', img_xy_dict)
    while len(os.listdir('static/images')) == 0:
        time.sleep(1)
    return render_template('showEffRes.html', url=url, name=name, x=x, y=y)


@app.route('/img')
def sendImg():
    global haveSent
    if haveSent == True:
        return "empty"
    try:
        img_path = os.listdir('zwz_sending')[0]
        img_name = img_path.split('/')[-1]
        haveSent = True
    except:
        return "empty"
    
    return send_from_directory("zwz_sending/", img_name, as_attachment=True)

@app.route('/returnimg', methods=['POST'])
def postImage():
    b64ImgData = request.form['imgData']
    filename = request.form['filename']
 
    with open('static/images/' + filename, 'wb') as f:
        imgData = base64.b64decode(b64ImgData)
        f.write(imgData)
    return 'ok'

# 清空文件夹
def del_files(dir_path):
    for root, _, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))  # 删除文件


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    # del_files('photos')
    # server = pywsgi.WSGIServer(('0.0.0.0',80),app)
    # server.serve_forever()
    del_files('photos')
    app.run()
