import pandas as pd #数据分析
import numpy as np #科学计算
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from flask import Flask
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.ensemble import GradientBoostingClassifier
import os
import csv
import uuid
from pai_algorithm.pre import csv_util
@csrf_exempt
def gdbt_importance(request):
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
        gbdt = GradientBoostingClassifier(
            init=None,
            learning_rate=0.1,
            loss='deviance',
            max_depth=3,
            max_features=None,
            max_leaf_nodes=None,
            min_samples_leaf=1,
            min_samples_split=2,
            min_weight_fraction_leaf=0.0,
            n_estimators=100,
            random_state=None,
            subsample=1.0,
            verbose=0,
            warm_start=False)
        gbdt.fit(x_train, y_train)
        importances = gbdt.feature_importances_
        # print (pca_data.tolist())
        result = {"importances": importances.tolist()}
        return HttpResponse(json.dumps(result), content_type="application/json")