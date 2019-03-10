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
# csv_file,target
@csrf_exempt
def standard(request):
    # 获取数据
    f = request.FILES.get("csv_file")
    filename = csv_util.upload(f)
    data_train = pd.read_csv(filename)

    # target是标准化的目标列名
    target = request.POST['target']
    target_df=data_train[target] #取出目标列数据
    scaler = preprocessing.StandardScaler()
    standard_data = scaler.fit_transform(data_train[target])
    data_train.drop([target],axis=1,inplace=True)
    data_train[target] = standard_data
    return_filename = csv_util.save(data_train)
    response = HttpResponse(csv_util.file_iterator(return_filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result.csv"'
    # 删除临时数据
    os.remove(filename)
    os.remove(return_filename)
    return response





if __name__ == "__main__":
    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
    app.run(debug=True)