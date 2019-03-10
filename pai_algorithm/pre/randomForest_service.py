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
from sklearn.ensemble import RandomForestRegressor
# csv_file,target,ref
@csrf_exempt
def randomForest(request):
    # 获取数据
    f = request.FILES.get("csv_file")
    filename = csv_util.upload(f)
    data_train = pd.read_csv(filename)

    # target是补全的目标列名
    target = request.POST['target']
    # ref是用来生成拟合值的相关项列表,格式是以逗号将各项隔开的字符串，如：SibSp,Pclass,Fare,Parch
    ref_str = request.POST['ref']
    ref = ref_str.split(',')
    ref.insert(0,target)#将target列名插入在ref最前面
    target_df=data_train[ref]#将这些列的数据都取出来
    #将数据分成已知目标项值和未知目标项值两部分
    known_data= target_df[target_df[target].notnull()].as_matrix()
    unknown_data =  target_df[target_df[target].isnull()].as_matrix()
    # y即目标值
    y = known_data[:, 0]
    # X即特征属性值
    X = known_data[:, 1:]
    # fit到RandomForestRegressor之中
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)
    # 用得到的模型进行未知目标值结果预测
    predictedAges = rfr.predict(unknown_data[:, 1::])
    # 用得到的预测结果填补原缺失数据
    data_train.loc[(data_train[target].isnull()), target] = predictedAges

    return_filename = csv_util.save(data_train)
    response = HttpResponse(csv_util.file_iterator(return_filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result.csv"'
    # 删除临时数据
    os.remove(filename)
    os.remove(return_filename)
    return response
