from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from blog.models import Blog, Tag
from authority.models import User
from mysite import settings
import re

# Create your views here.


def archive(request):
	if 'level' in request.session:
		level = request.session['level']
	else:
		level = 1000
	blogs = Blog.objects.filter(view_level__gte = level).order_by('-date')
	context = {'site': settings.SITE, 'session': request.session, 'blogs' : blogs}
	return render(request, 'blog/archive.html', context)


def index(request):
	context = {'site': settings.SITE, 'session': request.session}
	return render(request, 'mysite/base.html', context)


def blog(request):
	path = re.match('.*/([^/]*)$', request.path).group(1)
	if path == '':
		return HttpResponseRedirect('/')
	blog = Blog.get_blog_path(path)
	user = User.get_user_session(request.session)
	if request.method == 'POST':
		Blog.try_save(request.POST, path, user, blog, settings.SITE.get("public"))
		return HttpResponse('success')
	
	if blog is None:
		if user is None:
			return HttpResponse('blog not exist')
		if (not settings.SITE.get("public")) and (user.access_level > 1):
			return HttpResponse('blog not exist')
		if 'edit' in request.GET:
			return edit_blog(request, blog)
		return HttpResponseRedirect(path + '?edit=');
	else :
		if 'edit' in request.GET:
			if (not settings.SITE.get("public"))or(user is None):
				if user != blog.owner: 
					return HttpResponse("you can't edit this blog")
			return edit_blog(request, blog)
		return read_blog(request, blog, user)


def edit_blog(request, blog):
	context = {'site': settings.SITE, 'session': request.session, 'blog':blog}
	return render(request, 'blog/blog_edit.html', context)

def read_blog(request, blog, user):
	if user is None:
		level = 1000
	else :
		level = user.access_level
	if (level > blog.view_level):
		return HttpResponse('blog not exist')
	context = {'site': settings.SITE, 'session': request.session, 'blog': blog, 'user':user}
	return render(request, 'blog/blog.html', context)


def getKey(obj):
	return obj.size

def tags(request):
	if 'level' in request.session:
		level = request.session['level']
	else:
		level = 1000

	tag_list = Tag.objects.all()
	tags = []
	for tag in tag_list:
		tag.blogs = Blog.objects.filter(tags__exact=tag, view_level__gte=level).order_by('-date')
		tag.size = len(tag.blogs)
		blogs = Blog.objects.filter(tags__exact=tag)
	tags =  sorted(tag_list, key=getKey, reverse=True)
	context = {'site': settings.SITE, 'session': request.session, 'tags': tags}
	return render(request, 'blog/tags.html', context)