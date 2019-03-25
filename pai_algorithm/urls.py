"""pai_algorithm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from pai_algorithm.evaluate_server import confusion_matrix_server
from .evaluate_server import cluster_evaluation_server
from .evaluate_server import regression_evaluation_server
from .ml_service import GBDT_regression_server
from .ml_service import GBDT_service
from .ml_service import KMeans_server
from .ml_service import gaussianNB_server
from .ml_service import knn_service
from .ml_service import linear_regression_server
from .ml_service import logistic_regression_service
from .ml_service import random_forest_service
from .ml_service import svm_service
from .evaluate_server import two_category_division_server
from .evaluate_server import multy_category_division_server
from .pre import id_service
from .pre import normalize_service
from .pre import standard_service
from .pre import randomForest_service
from .pre import format_service
from .text_server import participles_server
from .text_server import stop_words_server
from .text_server import kv_server
from .text_server import lda_server

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^svm/$',svm_service.svm),
    url(r'^lr/$',logistic_regression_service.lr),
    url(r'^knn/$',knn_service.knn),
    url(r'^rf/$',random_forest_service.rf),
    url(r'^nb/$', gaussianNB_server.nb),
    url(r'^GBDT/$', GBDT_service.gbdt),
    url(r'^linear/$', linear_regression_server.linear),
    url(r'^GBDT_regression/$', GBDT_regression_server.train),
    url(r'^KMeans/$', KMeans_server.train),
    url(r'^cm/$', confusion_matrix_server.train),
    url(r'^ce/$', cluster_evaluation_server.value),
    url(r'^re/$', regression_evaluation_server.value),
    url(r'^tcd/$', two_category_division_server.value),
    url(r'^mcd/$', multy_category_division_server.value),
    url(r'^setId/$', id_service.setId),
    url(r'^normalize/$', normalize_service.normalize),
    url(r'^standard/$', standard_service.standard),
    url(r'^randomForest/$', randomForest_service.randomForest),
    url(r'^format/$', format_service.format),
    url(r'^par/$', participles_server.operate),
    url(r'^sw/$', stop_words_server.operate),
    url(r'^kv/$', kv_server.operate),
    url(r'^lda/$', lda_server.lda),

]
