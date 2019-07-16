from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append('..')

from controller.models import ControllerInput
from sensors.models import SensorData

from json import dumps
# Create your views here.

"""
    This will return both the controller and sensor data for the robot
    Probably don't need to make an entire app for it, but here we are
"""
def index(request):
    c = ControllerInput.objects.get(id=1).createDictionary()
    s = SensorData.objects.get(id=1).createDictionary()
    cs_tuple = (c, s)
    return HttpResponse(dumps(cs_tuple))