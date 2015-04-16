from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^file/', include('file.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^', include('blog.urls')),
)
