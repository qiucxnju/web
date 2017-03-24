from django.conf.urls import *
from talos import views

urlpatterns = [
    url(r'^setGamepad', views.setGamepad, name='index'),
    url(r'^getGamepad', views.getGamepad, name='index'),
    url(r'^setFrame', views.setFrame, name='index'),
    url(r'^getFrame', views.getFrame, name='index'),
    url(r'^', views.index, name='index'),
]
