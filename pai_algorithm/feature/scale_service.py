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
def scale_(request):
    if "POST" == request.method:
        # 获取数据
        f = request.FILES.get("csv_file")
        filename=csv_util.upload(f)
        data_train=pd.read_csv(filename)
        os.remove(filename)
        #尺度变换目标列名
        target_str = request.POST['target']
        target = target_str.split(',')
        # 尺度变换方法：log2、log10、ln、abs、sqrt
        scale=request.POST['scale']
        for each in target:
            target_df = data_train[each]
            if scale=='log2':
                data_train[each]=np.log2(target_df)
            elif scale=='log10':
                data_train[each] = np.log10(target_df)
            elif scale == 'ln':
                data_train[each] = np.log(target_df)
            elif scale == 'abs':
                data_train[each] = np.abs(target_df)
            elif scale == 'sqrt':
                data_train[each] = np.sqrt(target_df)
            else:
                print('wrong')
                result = {"status": 'wrong',
                          "reason": '输入的方法不包含在log2、log10、ln、abs、sqrt里'}
                return HttpResponse(json.dumps(result), content_type="application/json")
        print (data_train)
        return_filename = csv_util.save(data_train)
        response = HttpResponse(csv_util.file_iterator(return_filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="result.csv"'
        os.remove(return_filename)
        return response