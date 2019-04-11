from sklearn.model_selection import train_test_split
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np #科学计算
@csrf_exempt
def split(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']
    Y_train = json_result['y_train']
    test_per=json_result['test_size']
    random_num= json_result['random_state']
    X_train, X_test, y_train, y_test = train_test_split(X_train, Y_train, test_size=test_per,
                                                                         random_state=random_num)
    result = {"X_train":X_train,
              "y_train":y_train,
              "X_test":X_test,
              "y_test":y_test}
    return HttpResponse(json.dumps(result), content_type="application/json")