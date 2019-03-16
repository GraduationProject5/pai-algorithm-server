import pandas as pd #数据分析
import numpy as np #科学计算
import sklearn.preprocessing as preprocessing
from flask import Flask
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression
import os
import csv
import uuid
from pai_algorithm.pre import csv_util
# 将数据转换为x_train,y_train形式
# csv_file为上传的数据文件，flag是作为标签的数据列名
@csrf_exempt
def format(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)

        # flag是作为标签的属性名
        flag = request.POST['flag']

        y_train=data_train[flag].values.tolist()
        x_train=data_train.drop(flag, 1).values.tolist()

        print(x_train)
        print(y_train)

        result = {"X_train": x_train,
                  "Y_train": y_train}
        return HttpResponse(json.dumps(result), content_type="application/json")