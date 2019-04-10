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
from pai_algorithm.pre import response_util
# 将数据转换为x_train,y_train形式
# csv_file为上传的数据文件，flag是作为标签的数据列名
@csrf_exempt
def format(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        # label是作为标签的属性名
        label = request.POST['label']
        y_train = data_train[label].values.tolist()
        # 是否除了标签列外的所有列都需要
        all_used = request.POST['all_used']
        if all_used=='0':
            # data_col 是需要的数据列名
            data_col_str=request.POST['data_col']
            data_col = data_col_str.split(',')
            x_train=data_train[data_col]
            result = {"X_train": x_train,
                      "Y_train": y_train}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            x_train=data_train.drop(label, 1).values.tolist()
            result = {"X_train": x_train,
                      "Y_train": y_train}
            return HttpResponse(json.dumps(result), content_type="application/json")