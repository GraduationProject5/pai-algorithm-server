import json

import jieba
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


@csrf_exempt
def operate(request):
    postBody = request.body
    json_result = json.loads(postBody)
    text = json_result['text']
    seg_list = jieba.lcut(text,cut_all=False)



    result = {"seg_list":seg_list}
    return HttpResponse(json.dumps(result), content_type="application/json")
