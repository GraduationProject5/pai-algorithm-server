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
    seg_list = json_result['seg_list']
    stop_list = json_result['stop_list']
    stopped_tokens = [i for i in seg_list if not i in stop_list]



    result = {"stopped_tokens":stopped_tokens}
    return HttpResponse(json.dumps(result), content_type="application/json")
