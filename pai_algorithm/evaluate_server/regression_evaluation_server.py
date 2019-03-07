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

    explained_variance_score= sklearn.metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error = sklearn.metrics.mean_absolute_error(y_true, y_pred)
    mean_squared_error = sklearn.metrics.mean_squared_error(y_true, y_pred)
    median_absolute_error = sklearn.metrics.median_absolute_error(y_true, y_pred)
    r2_score = sklearn.metrics.r2_score(y_true, y_pred)

    result = {
        "explained_variance_score": explained_variance_score,
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "median_absolute_error": median_absolute_error,
        "r2_score": r2_score

    }

    return HttpResponse(json.dumps(result), content_type="application/json")