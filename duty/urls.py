from django.conf.urls import *

from duty import views

urlpatterns = [
    url(r'^list$', views.listRule, name='index'),
    url(r'^add$', views.addRule, name= 'index'),
    url(r'^', views.duty, name= 'index'),
]
