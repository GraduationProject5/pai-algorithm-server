import pandas as pd #数据分析
import numpy as np #科学计算
from flask import Flask
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import csv
import uuid
from pai_algorithm.pre import csv_util
from pai_algorithm.pre import response_util
# csv_file,target
@csrf_exempt
def soften(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        #平滑目标列名
        target= request.POST['target']
        # 平滑方法:百分位 per 、阈值 thresh
        soften_method=request.POST['soften_method']
        # 上下数据点（上下百分位或最大最小阈值）
        min_value=int(request.POST['min'])
        max_value = int(request.POST['max'])
        # 取出目标数据
        target_df = data_train[target].values.tolist()
        if soften_method=='per':
            # 百分位平滑
            if min_value<0:
                return response_util.wrong_info('百分位平滑，min值应不小于0')
            elif max_value>100:
                return response_util.wrong_info('百分位平滑，max值应不大于100')
            else:
                min_value/=100
                max_value/=100
                # 列表中最小最大值
                data_min=min(target_df)
                data_max=max(target_df)
                # 计算出来的范围
                min_num=data_min+min_value*(data_max-data_min)
                max_num=data_min+max_value*(data_max-data_min)
                for i in range(0, len(target_df)):
                    if target_df[i]<min_num:
                        target_df[i]=min_num
                    elif target_df[i]>max_num:
                        target_df[i]=max_num
                data_train[target]=target_df
        elif soften_method=='thresh':
            # 阈值平滑
            for i in range(0, len(target_df)):
                if target_df[i] < min_value:
                    target_df[i] = min_value
                elif target_df[i] > max_value:
                    target_df[i] = max_value
            data_train[target] = target_df
        else:
            return response_util.wrong_info('输入的方法不包含在per/thresh里')
        return response_util.csv_info(data_train)