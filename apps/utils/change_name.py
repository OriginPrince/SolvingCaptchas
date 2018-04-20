# _*_ encoding:utf-8 _*_
# author:ElegyPrincess


from RecognizeCaptcha.settings import BASE_DIR
import glob
import os

if __name__=="__main__":
    captcha_image_files = glob.glob(os.path.join(BASE_DIR, 'media', 'train', "*"))
    for captcha_image_file in captcha_image_files:
        filename = os.path.basename(captcha_image_file)
        captcha_correct_text = os.path.splitext(filename)[0]
        newName=os.path.join(os.path.join(BASE_DIR, 'media', 'train'),captcha_correct_text.upper()+".png")
        os.rename(captcha_image_file,newName)