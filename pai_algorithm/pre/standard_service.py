import pandas as pd #数据分析
import numpy as np #科学计算i
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
# csv_file,target
@csrf_exempt
def standard(request):
    # 获取数据
    f = request.FILES.get("csv_file")
    filename = csv_util.upload(f)
    data_train = pd.read_csv(filename)
    os.remove(filename)
    # target是标准化的目标列名
    target_str = request.POST['target']
    target = target_str.split(',')
    scaler = preprocessing.StandardScaler()
    for each in target:
        standard_data = scaler.fit_transform(data_train[each])
        data_train.drop([each], axis=1, inplace=True)
        data_train[each] = standard_data
    return response_util.csv_info(data_train)
