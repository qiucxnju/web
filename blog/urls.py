from django.conf.urls import patterns, url

from blog import views
from blog import ajax

urlpatterns = patterns('',
    url(r'^archive', views.archive, name='index'),
    url(r'^tags', views.tags, name= 'index'),
    url(r'^$', views.index, name='index'),
    url(r'^ajax/loadTags', ajax.loadTags, name='index'),
    url(r'^blog', views.blog, name='index'),
)
