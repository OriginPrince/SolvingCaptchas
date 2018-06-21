# SolvingCaptchas
本文实现了一个验证码识别系统，基于Django，使用django-simple-captcha来生成验证码，使用Keras来搭建卷积神经网络模型。构建了方便用户使用的识别界面   
在使用之前，需要生成django-simple-captcha需要的模型。   
使用命令：   
makemigrations   
migrate   
各个文件的作用：   
ProduceData文件包：生成训练数据，保存在media/train中，使用url：localhost:8000/getData   
CoverData文件包：处理数据：SplitData.py降噪图片并分割，ResizeData.py处理图片尺寸，TrainModel.py训练模型，保存到media中   
RecognizeData文件包：识别验证码内容函数：   
Home：用户测试界面 使用url：localhost:8000/home   
