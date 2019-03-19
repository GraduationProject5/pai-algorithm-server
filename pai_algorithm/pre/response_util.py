import os
import csv
import uuid
import pandas as pd #数据分析
import json
from pai_algorithm.pre import csv_util
from django.http import HttpResponse
def wrong_info(info):
    result={'status':'wrong',
            'reason':info}
    return HttpResponse(json.dumps(result), content_type="application/json")

def csv_info(data):
    return_filename = csv_util.save(data)
    response = HttpResponse(csv_util.file_iterator(return_filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result.csv"'
    os.remove(return_filename)
    return response