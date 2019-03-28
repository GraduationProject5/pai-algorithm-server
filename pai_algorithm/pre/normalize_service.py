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
# csv_file,target
@csrf_exempt
def normalize(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        #归一化目标列名
        target=request.POST['target']
        # 取出目标列数据
        mm = preprocessing.MinMaxScaler()  # 归一化
        target_str = request.POST['target']
        target = target_str.split(',')
        for each in target:
            mm_data = mm.fit_transform(data_train[each])  # 处理数据
            data_train.drop([each], axis=1, inplace=True)
            data_train[each] = mm_data
        return response_util.csv_info(data_train)

        # return HttpResponse(json.dumps(data_train.to_csv()), content_type="application/json")