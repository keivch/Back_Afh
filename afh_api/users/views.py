from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .Serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.middleware.csrf import get_token

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = Users.objects.all()


