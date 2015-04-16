from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from blog.models import Blog, Tag
from authority.models import User
from file.models import File
from mysite import settings

# Create your views here.


def upload(request):
	user = User.get_user_session(request.session)


	if (user == None):
		return HttpResponse("you can't upload file, please login")

	if user.access_level > 1:
			return HttpResponse("you don't have authority to upload file")

	if request.method == 'POST':
		dir = File.try_save(request.POST, request.FILES['file'], user)
		return HttpResponse('Your file path is<br><a href="/%s%s">/%s%s</a><br>It can be directly pasted in a wiki link.' % (settings.FILE_DIR, dir, settings.FILE_DIR, dir) )
	context = {'site': settings.SITE, 'session': request.session}
	return render(request, 'file/upload.html', context)


def list(request):
	user = User.get_user_session(request.session)
	if user is None:
		return HttpResponseRedirect('/')
	files = File.objects.filter(owner = user)
	context = {'file_dir':settings.FILE_DIR, 'site': settings.SITE, 'session': request.session, 'files': files}
	return render(request, 'file/list.html', context)
