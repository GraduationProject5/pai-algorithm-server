import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def create_exp(request):
    username=request.POST['username']
    exp_name=request.POST['exp_name']
    exp_dir = os.path.join('static', username,exp_name)
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)
    result = {'status': 'success',
              'reason': '成功创建实验文件夹'}
    return HttpResponse(json.dumps(result), content_type="application/json")


