import pandas as pd #数据分析
import numpy as np #科学计算
from flask import Flask
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression
import os
import csv
import uuid
from pai_algorithm.pre import csv_util
from sklearn.cluster import KMeans
from pai_algorithm.pre import response_util
# csv_file,target
@csrf_exempt
def discrete(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        #离散化目标列名
        target= request.POST['target']
        # 离散化方法:等频 frequency 、等距 metric、聚类 cluster
        discrete_method=request.POST['discrete_method']
        # 离散区间
        num=int(request.POST['num'])
        target_df = data_train[target]
        if discrete_method=='metric':
            # 等距离散化
            data_train[target]=pd.cut(target_df,num,labels = range(num))
        elif discrete_method=='frequency':
            # 等频率离散化
            w = [1.0 * i / num for i in range(num + 1)]
            w = target_df.describe(percentiles=w)[4:4 + num + 1]
            w[0] = w[0] * (1 - 1e-10)
            data_train[target] = pd.cut(target_df, w, labels=range(num))
        elif discrete_method=='cluster':
            #基于聚类的离散化
            kmodel = KMeans(n_clusters=num, n_jobs=4)  # n_jobs是并行数，一般等于CPU数
            kmodel.fit(target_df.values.reshape((len(target_df), 1)))
            c = pd.DataFrame(kmodel.cluster_centers_).sort_values(0)
            # rolling_mean表示移动平均，即用当前值和前2个数值取平均数，
            # 由于通过移动平均，会使得第一个数变为空值，因此需要使用.iloc[1:]过滤掉空值。
            w = c.rolling(2).mean().iloc[1:]
            w = [0] + list(w[0]) + [target_df.max()]  # 把首末边界点加上，首边界为0，末边界为data的最大值120000
            data_train[target] = pd.cut(target_df, w, labels=range(num))  # cut函数实现将data中的数据按照w的边界分类。
        else:
            return response_util.wrong_info('输入的方法不包含在frequency/metric/cluster里')
        return response_util.csv_info(data_train)