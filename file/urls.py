from django.conf.urls import *

from file import views

urlpatterns = [
    url(r'^upload', views.upload, name='index'),
    url(r'^list', views.list, name='index'),
]
