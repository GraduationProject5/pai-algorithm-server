import pandas as pd #数据分析
import numpy as np #科学计算
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
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
def importance(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        # 评估重要性目标列名
        target_str = request.POST['target']
        target = target_str.split(',')
        x_train = data_train[target]  # 将这些列的数据都取出来
        # 标签列名
        label=request.POST['label']
        y_train=data_train[label]

        forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
        forest.fit(x_train, y_train)
        importances = forest.feature_importances_
        # print (pca_data.tolist())
        result = {"importances": importances.tolist()}
        return HttpResponse(json.dumps(result), content_type="application/json")