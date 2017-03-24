#coding: utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from authority.models import User
from mysite import settings
from duty.models import Rule

# Create your views here.
def listRule(request):
	rules = Rule.get_all(False)
	dutys = Rule.get_duty()
	print rules
	contents = {'site': settings.SITE, 'session': request.session, 'rules' : rules, 'dutys':dutys}
	return render(request, 'duty/list.html', contents)

def addRule(request):
	Rule.add_rule(request.POST)
	return HttpResponse('success')

def duty(request):
	dutys = Rule.get_duty()
	print dutys
	contents = {'site': settings.SITE, 'session': request.session, 'dutys':dutys}
	return render(request, 'duty/duty.html', contents)


