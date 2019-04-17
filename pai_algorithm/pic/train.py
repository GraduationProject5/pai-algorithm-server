import json
import os
from django.http import HttpResponse
from pai_algorithm.pre import response_util
import uuid
import tensorflow as tf
import random
import keras
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras import backend as K
from pai_algorithm.pic.load_dataset import load_dataset, resize_image

IMAGE_SIZE=64
@csrf_exempt
def train(request):
    username = request.POST['username']
    exp_name = request.POST['exp_name']
    #训练批次，默认15
    epoach=int(request.POST.get('epoach',15))
    #batch大小。默认64
    batch=int(request.POST.get('batch',64))
    file_dir=os.path.join('static', username, exp_name)

    model = Model()
    data = Dataset(file_dir)
    data.load(img_channels=3)
    model.build_model(dataset=data,nb_classes=data.nb_classes)
    history=model.train(dataset=data,batch_size=batch,nb_epoch=epoach)
    test_result=model.evaluate(dataset=data)

    result={
        'history':history.history,
        'test':test_result
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

class Dataset:
    # http://www.runoob.com/python3/python3-class.html
    # 很多类都倾向于将对象创建为有初始状态的。
    # 因此类可能会定义一个名为 __init__() 的特殊方法（构造方法），类定义了 __init__() 方法的话，类的实例化操作会自动调用 __init__() 方法。
    # __init__() 方法可以有参数，参数通过 __init__() 传递到类的实例化操作上，比如下面的参数path_name。
    # 类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是 self。
    # self 代表的是类的实例，代表当前对象的地址，而 self.class 则指向类。
    def __init__(self, path_name):
        # 训练集
        self.train_images = None
        self.train_labels = None

        # 测试集
        self.test_images = None
        self.test_labels = None

        # 数据集加载路径
        self.path_name = path_name

        # 当前库采用的维度顺序，包括rows，cols，channels，用于后续卷积神经网络模型中第一层卷积层的input_shape参数
        self.input_shape = None

        self.nb_classes=None
        # 加载数据集并按照交叉验证的原则划分数据集并进行相关预处理工作

    def load(self, img_rows=IMAGE_SIZE, img_cols=IMAGE_SIZE, img_channels=3):
        # 加载数据集到内存
        images, labels,nb_classes = load_dataset(self.path_name,IMAGE_SIZE)

        # 注意下面数据集的划分是随机的，所以每次运行程序的训练结果会不一样
        train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.3,
                                                                                random_state=random.randint(0, 100))

        #print(test_labels) # 确认了每次都不一样

        # tensorflow 作为后端，数据格式约定是channel_last，与这里数据本身的格式相符，如果是channel_first，就要对数据维度顺序进行一下调整
        if K.image_data_format == 'channel_first':
            train_images = train_images.reshape(train_images.shape[0], img_channels, img_rows, img_cols)
            test_images = test_images.reshape(test_images.shape[0], img_channels, img_rows, img_cols)
            self.input_shape = (img_channels, img_rows, img_cols)
        else:
            train_images = train_images.reshape(train_images.shape[0], img_rows, img_cols, img_channels)
            test_images = test_images.reshape(test_images.shape[0], img_rows, img_cols, img_channels)
            self.input_shape = (img_rows, img_cols, img_channels)

        # 输出训练集和测试集的数量
        # print(train_images.shape[0], 'train samples')
        # print(test_images.shape[0], 'test samples')

        # 后面模型中会使用categorical_crossentropy作为损失函数，这里要对类别标签进行One-hot编码
        train_labels = keras.utils.to_categorical(train_labels, nb_classes)
        test_labels = keras.utils.to_categorical(test_labels, nb_classes)

        # 图像归一化，将图像的各像素值归一化到0~1区间。
        train_images /= 255
        test_images /= 255

        self.nb_classes=nb_classes
        self.train_images = train_images
        self.test_images = test_images
        self.train_labels = train_labels
        self.test_labels = test_labels

#建立卷积神经网络模型
class Model:
    # 初始化构造方法
    def __init__(self):
        self.model = None
    # 建立模型,nb_classes为类别数目
    def build_model(self, dataset,nb_classes):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), padding = 'same', input_shape = dataset.input_shape)) # 当使用该层作为模型第一层时，需要提供 input_shape 参数 （整数元组，不包含batch_size）
        self.model.add(Activation('relu'))
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size = (2,2))) # strides默认等于pool_size
        self.model.add(Conv2D(64, (3, 3), padding = 'same'))
        self.model.add(Activation('relu'))
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size = (2,2)))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.25))
        self.model.add(Dense(nb_classes))
        self.model.add(Activation('softmax'))

# 训练模型
    def train(self, dataset, batch_size = 64, nb_epoch = 15, data_augmentation = False):
        # https://jovianlin.io/cat-crossentropy-vs-sparse-cat-crossentropy/
        # If your targets are one-hot encoded, use categorical_crossentropy, if your targets are integers, use sparse_categorical_crossentropy.
        self.model.compile(loss = 'categorical_crossentropy',
                           optimizer = 'ADAM',
                           metrics = ['accuracy'])

        if not data_augmentation:
            history=self.model.fit(dataset.train_images,
                           dataset.train_labels,
                           batch_size = batch_size,
                           epochs = nb_epoch,
                           shuffle = True,
                            verbose=0)
        # 图像预处理
        else:
            #是否使输入数据去中心化（均值为0），是否使输入数据的每个样本均值为0，是否数据标准化（输入数据除以数据集的标准差），是否将每个样本数据除以自身的标准差，是否对输入数据施以ZCA白化，数据提升时图片随机转动的角度(这里的范围为0～20)，数据提升时图片水平偏移的幅度（单位为图片宽度的占比，0~1之间的浮点数），和rotation一样在0~0.2之间随机取值，同上，只不过这里是垂直，随机水平翻转，不是对所有图片翻转，随机垂直翻转，同上
            # 每个epoch内都对每个样本以以下配置生成一个对应的增强样本，最终生成了1969*(1-0.3)=1378*10=13780个训练样本，因为下面配置的很多参数都是在一定范围内随机取值，因此每个epoch内生成的样本都不一样
            datagen = ImageDataGenerator(rotation_range = 20,
                                         width_shift_range  = 0.2,
                                         height_shift_range = 0.2,
                                         horizontal_flip = True)
            #计算数据增强所需要的统计数据，计算整个训练样本集的数量以用于特征值归一化、ZCA白化等处理
#            当且仅当 featurewise_center 或 featurewise_std_normalization 或 zca_whitening 设置为 True 时才需要。
            #利用生成器开始训练模型
            # flow方法输入原始训练数据，生成批量增强数据
            history=self.model.fit_generator(datagen.flow(dataset.train_images, dataset.train_labels,
                                                    batch_size = batch_size),steps_per_epoch=dataset.train_images.shape[0]/batch_size,
                                      epochs = nb_epoch # 这里注意keras2里参数名称是epochs而不是nb_epoch，否则会warning，参考https://stackoverflow.com/questions/46314003/keras-2-fit-generator-userwarning-steps-per-epoch-is-not-the-same-as-the-kera
                                      )
        return history
    def evaluate(self, dataset):
        score = self.model.evaluate(dataset.test_images, dataset.test_labels) # evaluate返回的结果是list，两个元素分别是test loss和test accuracy
        str = "%s: %.3f , acc : %.3f%s" % ('Test loss', score[0], score[1] * 100, '%')
        return str