import cv2
import pickle
import os.path
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense,Dropout
from apps.ConvertData.ResizeData import resize_to_fit
from RecognizeCaptcha.settings import BASE_DIR


LETTER_IMAGES_FOLDER = os.path.join(BASE_DIR, 'media', 'extract')
MODEL_FILENAME =os.path.join(BASE_DIR, 'media', 'captcha_model.hdf5')
MODEL_LABELS_FILENAME =os.path.join(BASE_DIR, 'media', 'model_labels.dat')

data = []
labels = []

# 对输入图片进行循环
for image_file in paths.list_images(LETTER_IMAGES_FOLDER):
    # 加载并将其转化为灰度值
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 调整字母尺寸为20*20
    image = resize_to_fit(image, 20, 20)

    # 给图片添加第三维来使用keras，灰度图只有一维，彩色图有三维
    image = np.expand_dims(image, axis=2)

    # 获取图片文件夹的名字
    label = image_file.split(os.path.sep)[-2]

    # 将字母图片和图片文件夹的标签加到data和labels中
    data.append(image)
    labels.append(label)


# 将灰度值转化到0到1之间
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

#将训练数据分为训练数据和测试数据
(X_train, X_valtest, Y_train, Y_valtest) = train_test_split(data, labels, test_size=0.3, random_state=0)
(X_val, X_test, Y_val, Y_test) = train_test_split(X_valtest, Y_valtest, test_size=0.5, random_state=0)

# 将labels转化为keras可以使用的独热码，LabelBinarizer可以将数据二值化，也就是将标签转化为独热码
'''
独热码是一种特殊的编码
0:1000000000
1:0100000000
2:0010000000
……
'''
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_val = lb.transform(Y_val)
Y_test = lb.transform(Y_test)

# 将标签转化的独热码字典进行保存，我们在使用神经网络预测值的时候需要使用独热码
with open(MODEL_LABELS_FILENAME, "wb") as f:
    pickle.dump(lb, f)

# 开始创建神经网络
model = Sequential()

# 第一层卷积层和pooling层
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# 第二层卷积层和pooling层
model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# 汇合层
model.add(Flatten())
model.add(Dense(500, activation="relu"))

# 输出层
model.add(Dense(26, activation="softmax"))

# 让keras创建tensorflow model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# 训练神经网络
model.fit(X_train, Y_train, validation_data=(X_val, Y_val), batch_size=30, epochs=15, verbose=1)

scores=model.evaluate(X_test,Y_test)
print("+++++++++++++++++++++++")
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
# 将训练模型保存到磁盘
model.save(MODEL_FILENAME)
