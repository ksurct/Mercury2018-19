from api.models import ControllerInput
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


def list_input(request):
    

class ListControllerInput(APIView):
    def get(self, request, format=None):
        #This is where you return the controller input
        #input = ControllerInput.objects.all()
        #return Response(input)

    
