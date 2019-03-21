import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


@csrf_exempt
def lda(request):
    postBody = request.body
    json_result = json.loads(postBody)
    corpus = json_result['corpus']
    n_topics= json_result['n_topics']

    cntVector = CountVectorizer()
    cntTf = cntVector.fit_transform(corpus)
    print(cntTf)

    lda = LatentDirichletAllocation(n_topics=n_topics,
                                    learning_offset=50.,
                                    random_state=0)
    docres = lda.fit_transform(cntTf)
    print(docres)

    result = {"docres":docres.tolist()}
    return HttpResponse(json.dumps(result), content_type="application/json")
