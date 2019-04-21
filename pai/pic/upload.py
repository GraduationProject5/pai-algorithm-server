import json
import os
from django.http import HttpResponse
from pai_algorithm.pre import response_util
import uuid
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def upload(request):
    username=request.POST['username']
    exp_name=request.POST['exp_name']
    dir_name=request.POST['dir_name']
    class_dir = os.path.join('static', username,exp_name,dir_name)
    if not os.path.exists(class_dir):
        return response_util.wrong_info("不存在该实验或训练集目录")
    files=request.FILES.getlist('files')
    if len(files)>0:
        for file in files:
            filename = os.path.join(class_dir, file.name)
            with open(filename,'wb') as f:
                for c in file.chunks():
                    f.write(c)
    return response_util.success_info('成功上传图片')