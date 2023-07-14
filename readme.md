# 保留背景的图像风格迁移

## AnimeGANv2 + SAM 运行方法

**由于本人把这个模型集成到网页里了，要运行AnimeGANv2 + SAM应该要回退到之前的代码版本**
1. 安装python、pytorch、numpy、opencv等环境
2. 按照教程安装SAM：https://github.com/facebookresearch/segment-anything
3. 克隆本仓库
4. 在[SAM](https://github.com/facebookresearch/segment-anything#model-checkpoints)，[AnimeGANv2](https://github.com/bryandlee/animegan2-pytorch/tree/main/weights)中，下载权重。SAM的权重放在`test_withsam.py`同级，AnimeGANv2的权重放在`\animegan2-pytorch\weights`文件夹中。当然，权重的路径可以在代码中修改
5. 在`test_withsam.py`中修改`IMAGE_PATH`变量为需要风格迁移的图片路径
6. 用终端在`animegan2-pytorch`中，运行`python test_withsam.py`，即可看到分割过程与最终结果。注意，关闭过程可视化图片后程序才会继续运行

### 运行效果

![原图](/animegan2-pytorch/samples/results/拼图.jpg "原图")

# flask使用方法

[有bug先看这里](https://blog.csdn.net/qq_39548074/article/details/104414158)
## hello world!
1. 进入flask-test文件夹
2. 运行`python test.py`
3. 将终端中的网址打开，即可看到网页"hello, world!"

## 显示静态图片
1. 静态图片必须放在static文件夹下
2. 运行`python test.py`
3. 在终端中网址后加上“/hello”即可进入显示图片的页面
## 进行简单的分割+迁移网页部署
1. 首先要能成功运行 **AnimeGANv2 + SAM**
2. 进入flask-test文件夹，在终端运行`python test.py`
3. 在终端中网址后加上“/upload”即可进入上传图片的页面
4. 选择图片并上传
5. 等待**两分钟**
6. 网页输出风格迁移图片
> 注意，sam的prompt还不能在网页中修改，需要到代码里修改提示点的位置才能分割不同位置的物体

网站效果
![网站](flask-test/demo/proc1.png)

原图
![原图](flask-test/demo/jms.jpg)

网站生成图片
![网站生成](flask-test/demo/proc2.png)