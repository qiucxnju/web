from django.conf.urls import *

from authority import views

urlpatterns = [
    url(r'^logout', views.logout, name='index'),
    url(r'^login', views.login, name='index'),
    url(r'^register', views.register, name='index'),
]
