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
def setId(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        # 删除临时数据
        os.remove(filename)
        # 增加id列
        count = len(data_train)
        list = []
        for num in range(0, count):
            list.append(num)
        data_train.insert(0, 'id', list)
        return_filename = csv_util.save(data_train)
        response = HttpResponse(csv_util.file_iterator(return_filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="result.csv"'
        os.remove(filename)
        os.remove(return_filename)
        return response