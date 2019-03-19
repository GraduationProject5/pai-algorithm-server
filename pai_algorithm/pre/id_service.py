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
@csrf_exempt
def setId(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        # 增加id列
        count = len(data_train)
        list = []
        for num in range(0, count):
            list.append(num)
        data_train.insert(0, 'id', list)
        return response_util.csv_info(data_train)