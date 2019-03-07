import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression, LinearRegression


@csrf_exempt
def linear(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']
    y_train = json_result['y_train']
    X_test = json_result['X_test']


    lr = LinearRegression()
    re = lr.fit(X_train, y_train)

    lr.predict(X_test)


    result = {"prediction_result":lr.predict(X_test).tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
