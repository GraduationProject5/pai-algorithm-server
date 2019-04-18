import json
import os
from django.http import HttpResponse
from pai import models
from django.views.decorators.csrf import csrf_protect, csrf_exempt
#
#
def save_result(username,train,result):
    result_ob=models.TrainResult()
    result_ob.username=username
    result_ob.train=train
    result_ob.result=result
    result_ob.save()
    return result_ob.id

@csrf_exempt
def getResult(request):
    tid=int(request.POST.get('id'))
    result_ob=models.TrainResult.objects.get(id=tid)
    result = {'status': 'success',
              'result': result_ob.result}
    return HttpResponse(json.dumps(result), content_type="application/json")
