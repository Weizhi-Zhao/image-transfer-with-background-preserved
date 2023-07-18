from flask import Flask, request, redirect, render_template, url_for, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import cv2
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../animegan2-pytorch'))
import test_withsam
app = Flask(__name__)

app.config['UPLOADED_PHOTO_DEST'] = os.path.join(os.getcwd(), 'photos') # 当前工作目录
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
# def dest(name):
#     return '{}/{}'.format(UPLOAD_DEFAULT_DEST, name)

photos = UploadSet('PHOTO', IMAGES) # 大概是给上传的文件分类，然后限制上传文件类型
configure_uploads(app, photos) # 大概是初始化一下

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # TODO 这段程序具体还没搞懂
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo']) # 好像'photo'就是上传的文件名
        return redirect(url_for('show', name=filename))
    return render_template('upload.html')

@app.route('/photo/<name>')
def show(name):
    if name is None:
        abort(404)
    url = photos.url(name) # 对photos这个set调用.url()方法，即可获取文件（具体的不懂）
    img = cv2.imread(os.path.join('photos', name), cv2.IMREAD_COLOR)
    test_withsam.transfer_image(img, '')
    # cv2.imshow('result', img)
    # cv2.waitKey(0)
    return render_template('show.html', url=url, name=name)



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/hello")
def hello():
    return render_template("hello_world.html")

# 清空文件夹
def del_files(dir_path):
    for root, _, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))  # 删除文件

if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    del_files('photos')
    app.run() 