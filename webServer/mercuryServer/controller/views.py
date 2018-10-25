from django.shortcuts import render
from django.http import HttpResponse
from .models import ControllerInput
import json

# Create your views here.

def index(request):
    return HttpResponse(ControllerInput.objects.get(id=1))

def get(request):
    return HttpResponse(json.dumps(ControllerInput.objects.get(id=1).createDictionary()))

def update(request, dictionary):
    d = json.loads(dictionary)
    controller = ControllerInput.objects.get(id=1)

    print(controller.a)
    #c = ControllerInput.objects.get(id=1)
    print(d['a'])
    for item in d:
        setattr(controller, item, d[item])
    controller.save()
    print(controller.a)
    return HttpResponse("Values saved.")
