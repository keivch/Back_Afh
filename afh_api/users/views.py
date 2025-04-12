from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .Serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = Users.objects.all()


@api_view(['POST'])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')


    if not first_name and last_name and email and password and role:
        return Response({'error': 'enviar todos los datos'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email = email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=email,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    Users.objects.create(
        user = user,
        role = role
    )

    return Response({'Usuario registrado'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    user = User.objects.filter(email=email).first()
    type = Users.objects.filter(user = user).first()
    
    if not user or not user.check_password(password):
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generar o recuperar el token de autenticación
    token, created = Token.objects.get_or_create(user=user)
        
    csrf_token = get_token(request)
    
    return Response({'token': token.key, 'csrf_token': csrf_token, 'role': type.role}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Elimina el token del usuario actual
        request.user.auth_token.delete()
        return Response({"message": "Logout exitoso"}, status=200)
    except:
        return Response({"error": "Hubo un problema al cerrar sesión"}, status=400)