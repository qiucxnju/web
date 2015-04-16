from django.conf.urls import patterns, url

from authority import views

urlpatterns = patterns('',
    url(r'^logout', views.logout, name='index'),
    url(r'^login', views.login, name='index'),
    url(r'^register', views.register, name='index'),
)
