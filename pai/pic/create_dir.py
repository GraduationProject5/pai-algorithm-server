import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def create_train_dir(request):
    username=request.POST['username']
    exp_name=request.POST['exp_name']
    dir_name=request.POST['dir_name']
    class_dir = os.path.join('static', username,exp_name,dir_name)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
    result = {'status': 'success',
              'reason': '成功创建训练集文件夹'}
    return HttpResponse(json.dumps(result), content_type="application/json")