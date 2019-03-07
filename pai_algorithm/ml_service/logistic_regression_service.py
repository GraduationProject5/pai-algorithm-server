import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression


@csrf_exempt
def lr(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']
    y_train = json_result['y_train']
    X_test = json_result['X_test']

    tol = json_result['tol']
    c = json_result['c']
    penalty=json_result['penalty']

    lr = LogisticRegression(C=c,tol=tol,penalty=penalty)
    re = lr.fit(X_train, y_train)

    lr.predict(X_test)


    result = {"prediction_result":lr.predict(X_test).tolist(),"prediction_detail": re.predict_proba(X_test).tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
