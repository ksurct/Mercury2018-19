from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append('..')

from controller.models import ControllerInput
from sensors.models import SensorData

from json import dumps
# Create your views here.

def index(request):
    c = ControllerInput.objects.get(id=1).createDictionary()
    s = SensorData.objects.get(id=1).createDictionary()
    cs_tuple = (c, s)
    return HttpResponse(dumps(cs_tuple))