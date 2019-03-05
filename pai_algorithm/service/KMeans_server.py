import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


@csrf_exempt
def train(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']

    k = json_result['k']


    kn = KMeans(n_clusters=k)
    re = kn.fit(X_train)




    result = {"prediction_result":re.predict(X_train).tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
