from rest_framework import serializers
from .models import Users
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Users
        fields = '__all__'