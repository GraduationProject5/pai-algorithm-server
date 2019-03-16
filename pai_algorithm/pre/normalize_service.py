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
# csv_file,target
@csrf_exempt
def normalize(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)

        #归一化目标列名
        target=request.POST['target']
        # 取出目标列数据
        target_df = data_train[target]
        mm = preprocessing.MinMaxScaler()  # 归一化
        mm_data = mm.fit_transform(target_df)  # 处理数据
        data_train.drop([target], axis=1, inplace=True)
        data_train[target] = mm_data
        return_filename = csv_util.save(data_train)
        response = HttpResponse(csv_util.file_iterator(return_filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="result.csv"'
        os.remove(filename)
        os.remove(return_filename)
        return response

        # return HttpResponse(json.dumps(data_train.to_csv()), content_type="application/json")