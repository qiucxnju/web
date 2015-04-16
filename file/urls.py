from django.conf.urls import patterns, url

from file import views

urlpatterns = patterns('',
    url(r'^upload', views.upload, name='index'),
    url(r'^list', views.list, name='index'),
)
