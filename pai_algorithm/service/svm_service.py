import json

from django.contrib.sessions import serializers
from sklearn import svm

import numpy as np
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt


@csrf_exempt
def svm(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        tol=json_result['tol']
        c=json_result['c']
        practice_x = json_result['practice_x']
        practice_y = json_result['practice_y']

        test_x=json_result['test_x']
        #test_y=json_result['test_y']

        X = np.array(practice_x)
        y = np.array(practice_y)
        clt = svm.SVC(C=c,tol=tol)
        s = clt.fit(X, y)
        print(s.get_params())
        result_y = clt.predict(test_x)
        print(result_y)
        result = {"result_y": result_y.tolist()}
        return HttpResponse(json.dumps(result), content_type="application/json")
