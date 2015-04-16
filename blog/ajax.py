from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from blog.models import User, Blog, Tag
from mysite import settings
import re
import json

def loadTags(request):
	context = RequestContext(request)
	tags = json.loads(request.GET['tags'])
	ret_tags = []
	for tag in Tag.objects.all():
		value = tag.value
		if value not in tags:
			ret_tags.append(value)
	return HttpResponse(json.dumps(ret_tags))


	