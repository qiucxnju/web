from django.conf.urls import *

from blog import views
from blog import ajax

urlpatterns = [
    url(r'^archive', views.archive, name='index'),
    url(r'^tags', views.tags, name= 'index'),
    url(r'^$', views.archive, name='index'),
    url(r'^ajax/loadTags', ajax.loadTags, name='index'),
    url(r'^blog', views.blog, name='index'),
]
