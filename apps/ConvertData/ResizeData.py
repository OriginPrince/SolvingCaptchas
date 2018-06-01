# _*_ encoding:utf-8 _*_
# author:ElegyPrincess

import imutils
import cv2


def resize_to_fit(image, width, height):
    """
    调整图像为给定的尺寸
    :param image: 将要调整的图象
    :param width: 宽度
    :param height: 高度
    :return: 调整过后的图象
    """

    # 获取现有图片的高和宽
    (h, w) = image.shape[:2]

    # 如果宽度大于高度，将图片宽度置为给定的宽度
    if w > h:
        image = imutils.resize(image, width=width)

    # 如果宽度小于高度，将图片高度置为给定的高度
    else:
        image = imutils.resize(image, height=height)

    # 设置图片大小，将宽度或高度不够要求的进行填充
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # 给图片增加宽度或高度，重置图片尺寸来处理舍入问题
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))

    #返回处理后的图象
    return image