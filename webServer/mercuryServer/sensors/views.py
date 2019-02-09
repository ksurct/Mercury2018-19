from django.shortcuts import render
from django.http import HttpResponse
from .models import SensorData
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return HttpResponse(SensorData.objects.get(id=1))

def get(request):
    return HttpResponse(json.dumps(SensorData.objects.get(id=1).createDictionary()))

@csrf_exempt
def update(request, dictionary):
    d = json.loads(dictionary)
    sens = SensorData.objects.get(id=1)

    for item in d:
        setattr(sens, item, d[item])
    sens.save()
    return HttpResponse("values saved.")