import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sklearn


@csrf_exempt
def value(request):
    postBody = request.body
    json_result = json.loads(postBody)
    labels_true = json_result['labels_true']
    labels_pred = json_result['labels_pred']


    adjusted_Rand_index= sklearn.metrics.adjusted_rand_score(labels_true, labels_pred)
    mutual_information_based_scores= sklearn.metrics.adjusted_mutual_info_score(labels_true, labels_pred)
    homogeneity_score = sklearn.metrics.homogeneity_score(labels_true, labels_pred)
    completeness_score = sklearn.metrics.completeness_score(labels_true, labels_pred)
    v_measure_score = sklearn.metrics.v_measure_score(labels_true, labels_pred)
    fowlkes_mallows_score = sklearn.metrics.fowlkes_mallows_score(labels_true, labels_pred)

    result = {
        "adjusted_Rand_index": adjusted_Rand_index,
        "mutual_information_based_scores": mutual_information_based_scores,
        "homogeneity_score": homogeneity_score,
        "completeness_score": completeness_score,
        "v_measure_score": v_measure_score,
        "fowlkes_mallows_score": fowlkes_mallows_score
    }

    return HttpResponse(json.dumps(result), content_type="application/json")