import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


@csrf_exempt
def rf(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']
    y_train = json_result['y_train']
    X_test = json_result['X_test']
    n_estimators = json_result['n_estimators']
    rfc = RandomForestClassifier(n_estimators=n_estimators)


    re = rfc.fit(X_train, y_train)




    result = {"prediction_result":re.predict(X_test).tolist(),"prediction_detail": re.predict_proba(X_test).tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
