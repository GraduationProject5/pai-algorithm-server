import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression


@csrf_exempt
def train(request):
    postBody = request.body
    json_result = json.loads(postBody)
    X_train = json_result['X_train']
    y_train = json_result['y_train']
    X_test = json_result['X_test']

    loss = json_result['loss']
    learning_rate = json_result['learning_rate']
    n_estimators = json_result['n_estimators']
    subsample = json_result['subsample']
    min_samples_split = json_result['min_samples_split']
    min_samples_leaf = json_result['min_samples_leaf']
    max_depth = json_result['max_depth']
    alpha = json_result['alpha']
    verbose = json_result['verbose']
    lr = GradientBoostingRegressor(loss=loss,learning_rate=learning_rate,n_estimators=n_estimators,
                                    subsample=subsample,min_impurity_split=min_samples_split,
                                    min_samples_leaf=min_samples_leaf,max_depth=max_depth,
                                    alpha=alpha,verbose=verbose)
    re = lr.fit(X_train, y_train)

    lr.predict(X_test)


    result = {"prediction_result":lr.predict(X_test).tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
