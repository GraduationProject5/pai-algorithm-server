import json

import collections
import jieba
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier




@csrf_exempt
def operate(request):
    postBody = request.body
    json_result = json.loads(postBody)
    news_list = json_result['news_list']


    words=[]
    kvs={}

    count = 0
    for news in news_list:

        text=news["text"]
        word_counts = collections.Counter(text)

        kv={}
        for key in word_counts:

            if key not in words:
                words.append(key)
                loc=words.index(key);
                kv[loc] = word_counts[key]
            else:
                loc=words.index(key);
                kv[loc] = word_counts[key]

        print(kv)
        kvs[count] = kv

        count=count+1;



    print(words)


    result = {"kvs": kvs,
              "word_list":words
              }




    return HttpResponse(json.dumps(result), content_type="application/json")






