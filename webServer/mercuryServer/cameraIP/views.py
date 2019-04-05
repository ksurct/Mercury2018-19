from django.shortcuts import render
from django.http import HttpResponse
from .models import cameraIP
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse(cameraIP.objects.get(id=1))

@csrf_exempt
def update(request, newIP):
    c = cameraIP.objects.get(id=1)
    c.cameraIPstr = newIP
    c.save()
    return HttpResponse(cameraIP.objects.get(id=1))