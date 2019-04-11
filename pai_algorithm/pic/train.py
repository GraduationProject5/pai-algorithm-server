import json
import os
from django.http import HttpResponse
from pai_algorithm.pre import response_util
import uuid
import tensorflow as tf
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def train(request):
    username = request.POST['username']
    exp_name = request.POST['exp_name']
    file_dir=os.path.join('static', username, exp_name)

    return response_util.success_info('成功')