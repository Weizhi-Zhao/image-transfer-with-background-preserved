# 保留背景的图像风格迁移

## AnimeGANv2 + SAM 运行方法

1. 安装python、pytorch、numpy、opencv等环境
2. 按照教程安装SAM：https://github.com/facebookresearch/segment-anything
3. 克隆本仓库
4. 在[SAM](https://github.com/facebookresearch/segment-anything#model-checkpoints)，[AnimeGANv2](https://github.com/bryandlee/animegan2-pytorch/tree/main/weights)中，下载权重。SAM的权重放在`test_withsam.py`同级，AnimeGANv2的权重放在`\animegan2-pytorch\weights`文件夹中。当然，权重的路径可以在代码中修改
5. 在`test_withsam.py`中修改`IMAGE_PATH`变量为需要风格迁移的图片路径
6. 用终端在`animegan2-pytorch`中，运行`python test_withsam.py`，即可看到分割过程与最终结果。注意，关闭过程可视化图片后程序才会继续运行
