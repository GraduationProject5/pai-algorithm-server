import pandas as pd #数据分析
import numpy as np #科学计算
from sklearn.decomposition import PCA
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
def PCA_(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        # PCA需要使用的列名
        target_str = request.POST['target']
        target = target_str.split(',')
        target_df = data_train[target]  # 将这些列的数据都取出来
        # target_data=np.array(target_df)
        # print (target_data)
        # 进行主成分分析
        feature_num=int(request.POST['num'])
        pca = PCA(n_components=feature_num)
        pca_data = pca.fit_transform(target_df)
        # print (pca_data.tolist())
        result = {"pca_result": pca_data.tolist(),
                  "explained_variance_ratio_": pca.explained_variance_ratio_.tolist()}
        return HttpResponse(json.dumps(result), content_type="application/json")