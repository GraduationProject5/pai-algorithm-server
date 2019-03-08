import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sklearn


@csrf_exempt
def value(request):
    postBody = request.body
    json_result = json.loads(postBody)
    y_true = json_result['y_true']
    y_pred = json_result['y_pred']

    accuracy_score= sklearn.metrics.accuracy_score(y_true, y_pred, normalize=True, sample_weight=None)
    # roc_auc_score=sklearn.metrics.roc_auc_score(y_true, y_pred)
    classification_report = sklearn.metrics.classification_report(y_true, y_pred)

    result = {
        "accuracy_score": accuracy_score,
        # "roc_auc_score": roc_auc_score,
        "classification_report": classification_report


    }

    return HttpResponse(json.dumps(result), content_type="application/json")