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
@csrf_exempt
def dummy(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        # target_str为需要因子化的列名,以逗号隔开，例：cabin,sex,pclass
        target_str = request.POST['target']
        target = target_str.split(',')
        for each in target:
            dummies = pd.get_dummies(data_train[each], prefix=each)
            data_train = pd.concat([data_train, dummies], axis=1)
            data_train.drop([each], axis=1, inplace=True)
        return_filename = csv_util.save(data_train)
        response = HttpResponse(csv_util.file_iterator(return_filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="result.csv"'
        os.remove(return_filename)
        return response