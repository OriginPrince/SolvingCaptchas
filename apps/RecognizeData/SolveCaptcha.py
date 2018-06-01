# _*_ encoding:utf-8 _*_
# author:ElegyPrincess

from keras.models import load_model
from apps.ConvertData.ResizeData import resize_to_fit
from imutils import paths
import numpy as np
from apps.ConvertData.SplitData import interference_line,interference_point
import cv2
import pickle
import os
from RecognizeCaptcha.settings import BASE_DIR
from PIL import Image
import glob


MODEL_FILENAME = os.path.join(BASE_DIR, 'media', 'captcha_model.hdf5')
MODEL_LABELS_FILENAME = os.path.join(BASE_DIR, 'media', 'model_labels.dat')


# 加载模型标签，持久化
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)

# 加载训练好的神经网络模型
model = load_model(MODEL_FILENAME)

captcha_image_files = glob.glob(os.path.join(BASE_DIR,'media','test', "*"))
captcha_image_file=captcha_image_files[0]
save_path = os.path.join(BASE_DIR, 'media', 'extract_test')

img = cv2.imread(captcha_image_file)
height, width = img.shape[:2]

gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 给图片添加个边框
gray2 = cv2.copyMakeBorder(gray1, 2, 2, 2, 2, cv2.BORDER_REPLICATE)

gray = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# gray = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)

imga = interference_point(gray)
thresh, newname = interference_line(imga, "test.png","clean_test")

# 把去噪声后的图片进行分割
im = Image.open(newname)

subList = []
for i in range(0, 4):
    size = (0 + i * int(width * 0.25), 0, int(width * 0.25) * (i + 1), int(height))
    subImg = im.crop(size)
    subList.append(subImg)

    p = os.path.join(save_path, "{}.png".format(str(i)))
    subList[i].save(p)

predictions = []
for image_file in paths.list_images(save_path):
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Re-size the letter image to 20x20 pixels to match training data
    letter_image = resize_to_fit(image, 20, 20)

    # Turn the single image into a 4d list of images to make Keras happy
    letter_image = np.expand_dims(letter_image, axis=2)
    letter_image = np.expand_dims(letter_image, axis=0)

    # Ask the neural network to make a prediction
    prediction = model.predict(letter_image)

    # Convert the one-hot-encoded prediction back to a normal letter
    letter = lb.inverse_transform(prediction)[0]
    predictions.append(letter)

captcha_text = "".join(predictions)
print("CAPTCHA text is: {}".format(captcha_text))

cv2.imshow("image", img)
cv2.waitKey()
