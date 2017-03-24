from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from mysite import settings

import threading

class MyModel():
    gamepad = {}
    frame = None
    _gamepad_lock = threading.Lock()
    _camera_lock = threading.Lock()

    @classmethod
    def setGamepad(cls, gamepad):
        with cls._gamepad_lock:
            cls.gamepad = gamepad

    @classmethod
    def getGamepad(cls):
        with cls._gamepad_lock:
    	   return cls.gamepad

    @classmethod
    def getFrame(cls):
        with cls._camera_lock:
            return cls.frame
    @classmethod
    def setFrame(cls, frame):
        with cls._camera_lock:
            cls.frame = frame


x = MyModel()

def setGamepad(request):
	global x
	x.setGamepad(request.GET['gamepad'])
	return HttpResponse("success")

def getGamepad(request):
    global x
    return HttpResponse(x.getGamepad())

def setFrame(request):
    if request.method == 'GET':
        return render(request, 'talos/setFrame.html')
    global x
    print "setFrame"
    print request.body[-100:]
    x.setFrame(request.body)
    return HttpResponse("success")

def getFrame(request):
    global x
    print "getFrame"
    data = x.getFrame()
    print data[-100:]
    return HttpResponse(data, content_type='image/jpeg')

def index(request):
	context = {'site': settings.SITE, 'session': request.session}
	return render(request, 'talos/index.html', context)
