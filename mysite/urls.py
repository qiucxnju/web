from django.conf.urls import *
from django.contrib import admin
from django.conf.urls.static import static
from mysite import settings
import os

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^file/', include('file.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^talos/', include('talos.urls')),
    url(r'^duty/', include('duty.urls')),
    url(r'^', include('blog.urls')),
]
