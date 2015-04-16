from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from authority.models import User
from mysite import settings
import re

# Create your views here.
def register(request):
	if 'id' in request.session:
		return HttpResponseRedirect('/')
	if request.method == 'GET':
		context = {'site': settings.SITE}
		return render(request, 'authority/register.html', context)
	else:
		(ret, message) = User.try_save(request.POST)
		if ret:
			request.session['id'] = message.name
			request.session['name'] = message.realname
			request.session['level'] = message.access_level
			return HttpResponseRedirect('/')
		return HttpResponse(message)

def login(request):
	if 'id' in request.session:
		return HttpResponseRedirect('/')
	if request.method == 'GET':
		context = {'site': settings.SITE}
		return render(request, 'authority/login.html', context)
	else:
		(ret, message) = User.authenticate(request.POST)
		if (ret is not None):
			request.session['id'] = ret.name
			request.session['name'] = ret.realname
			request.session['level'] = ret.access_level
			return HttpResponseRedirect('/')
		else :
			return HttpResponse(message)

def logout(request):
	request.session.clear()
	return HttpResponseRedirect('/')