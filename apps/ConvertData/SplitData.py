# _*_ encoding:utf-8 _*_
# author:ElegyPrincess

from RecognizeCaptcha.settings import BASE_DIR
import cv2
import os
from PIL import Image
import glob


# 干扰线降噪
def interference_line(img, img_name,str='clean'):
    clean_image_files = os.path.join(BASE_DIR, 'media',str)
    filename = os.path.join(clean_image_files,img_name.split('.')[0] + '-c.jpg')
    h, w = img.shape[:2]
    # ！！！opencv矩阵点是反的
    # img[1,2] 1:图片的高度，2：图片的宽度
    for y in range(2, w - 2):
        for x in range(2, h - 2):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if img[x, y - 2] > 245:
                count = count + 1
            if img[x, y + 2] > 245:
                count = count + 1
            if img[x - 2, y] > 245:
                count = count + 1
            if img[x + 2, y] > 245:
                count = count + 1
            if count > 4:
                img[x, y] = 255
    for y in range(0, w):
        img[0,y]=255
        img[1,y]=255
        img[h-1, y] = 255
        img[h-2, y] = 255

    for x in range(0, h):
        img[x,0]=255
        img[x,1]=255
        img[x, w-1] = 255
        img[x, w-2] = 255

    cv2.imwrite(filename, img)
    return img,filename

# 点降噪
def interference_point(img, x=0, y=0):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img[x, y]  # 当前像素点的值
    height, width = img.shape[:2]

    for y in range(0, width - 1):
        for x in range(0, height - 1):
            if y == 0:  # 第一行
                if x == 0:  # 左上顶点,4邻域
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右上顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最上非顶点,6邻域
                    sum = int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            elif y == width - 1:  # 最下面一行
                if x == 0:  # 左下顶点
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x, y - 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右下顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y - 1])

                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最下非顶点,6邻域
                    sum = int(cur_pixel) \
                          + int(img[x - 1, y]) \
                          + int(img[x + 1, y]) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x + 1, y - 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            else:  # y不在边界
                if x == 0:  # 左边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                else:  # 具备9领域条件的
                    sum = int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 4 * 245:
                        img[x, y] = 0
    return img


if __name__=="__main__":
    captcha_image_files = glob.glob(os.path.join(BASE_DIR,'media','train', "*"))
    counts={}

    for captcha_image_file in captcha_image_files:
        filename=os.path.basename(captcha_image_file)
        captcha_correct_text = os.path.splitext(filename)[0]
        img = cv2.imread(captcha_image_file)
        height,width=img.shape[:2]

        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 给图片添加个边框
        gray2 = cv2.copyMakeBorder(gray1, 2, 2, 2, 2, cv2.BORDER_REPLICATE)

        gray = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #gray = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)

        imga = interference_point(gray)
        thresh,newname = interference_line(imga, filename)

        #把去噪声后的图片进行分割
        im=Image.open(newname)

        subList=[]
        for i in range(0,4):
            size=(0+i*int(width*0.25),0,int(width*0.25)*(i+1),int(height))
            subImg=im.crop(size)
            subList.append(subImg)

        for i in range(0,4):

            save_path = os.path.join(os.path.join(BASE_DIR, 'media', 'extract'), captcha_correct_text[i])

            # 路径不存在则创建
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # 获取该文件夹已经有多少张图片
            count = counts.get(captcha_correct_text[i], 1)
            p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))

            # 每个文件夹增加1
            counts[captcha_correct_text[i]] = count + 1
            subList[i].save(p)

