from django.shortcuts import render

# modules for rest api
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer

# Create your views here.


# rest api views

@api_view(['POST'])
def registration(request):
    pass

