from django.contrib import admin
from blog.models import User
from blog.models import Tag
from blog.models import Blog

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Blog)