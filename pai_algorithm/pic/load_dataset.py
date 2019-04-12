# import numpy as np #科学计算
# import cv2
# import os
#
# IMAGE_SIZE = 64  # 指定图像大小
#
# # 按指定图像大小调整尺寸
# def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
#     top, bottom, left, right = (0, 0, 0, 0)
#
#     # 获取图片尺寸
#     h, w, _ = image.shape
#
#     # 对于长宽不等的图片，找到最长的一边
#     longest_edge = max(h, w)
#
#     # 计算短边需要增加多少像素宽度才能与长边等长(相当于padding，长边的padding为0，短边才会有padding)
#     if h < longest_edge:
#         dh = longest_edge - h
#         top = dh // 2
#         bottom = dh - top
#     elif w < longest_edge:
#         dw = longest_edge - w
#         left = dw // 2
#         right = dw - left
#     else:
#         pass  # pass是空语句，是为了保持程序结构的完整性。pass不做任何事情，一般用做占位语句。
#
#     # RGB颜色
#     BLACK = [0, 0, 0]
#     # 给图片增加padding，使图片长、宽相等
#     # top, bottom, left, right分别是各个边界的宽度，cv2.BORDER_CONSTANT是一种border type，表示用相同的颜色填充
#     constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
#     # 调整图像大小并返回图像，目的是减少计算量和内存占用，提升训练速度
#     return cv2.resize(constant, (height, width))
#
# #读取数据，dir为实验目录，读取实验目录下的训练类别目录，并根据训练类别目录名称打标签
# def get_files(dir):
#     class_train = []
#     label_train = []
#     classes=[]
#     for train_class in os.listdir(dir):
#         class_path=os.path.join(dir,train_class)
#         classes.append(train_class)
#         for pic in os.listdir(class_path):
#             data = cv2.imread(os.path.join(class_path,pic))
#             image = resize_image(data, IMAGE_SIZE, IMAGE_SIZE)
#             class_train.append(image)
#             label_train.append(train_class)
#     return class_train,label_train,classes
#
# def load_dataset(path_name,t_size):
#     IMAGE_SIZE=t_size
#     images, labels,classes = get_files(path_name)
#     # 将lsit转换为numpy array
#     images = np.array(images, dtype='float')  # 注意这里要将数据类型设为float，否则后面face_train_keras.py里图像归一化的时候会报错
#     labels = np.array([classes.index(label) for label in labels])  # 根据类别转换为数字标签
#     # print(images.shape)
#     # print(labels)
#     return images, labels,len(classes)
#
#
#
