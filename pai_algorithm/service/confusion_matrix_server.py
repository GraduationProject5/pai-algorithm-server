import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sklearn


@csrf_exempt
def train(request):
    postBody = request.body
    json_result = json.loads(postBody)
    y_pred = json_result['y_pred']
    y_true = json_result['y_true']


    confusion_matrix=sklearn.metrics.confusion_matrix(y_true, y_pred)







    result = {
               "confusion_matrix": confusion_matrix.tolist()}

    return HttpResponse(json.dumps(result), content_type="application/json")