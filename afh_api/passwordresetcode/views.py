from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import PasswordResetCode
from django.conf import settings
from .Serializer import PasswordResetCodeSerializer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .Services import sendMailRecovery

class PasswordResetCodeViewSet(viewsets.ModelViewSet):
    serializer_class= PasswordResetCodeSerializer
    queryset = PasswordResetCode.objects.all()

@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        sendMailRecovery(email, user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'message': 'Código enviado al correo.', "Token": token.key}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'Correo no encontrado.'}, status=400)
    
@api_view(['POST'])
def validate_code(request):
    code = request.data.get('code')

    try:
        reset_code = PasswordResetCode.objects.filter(code = code).first()

        if reset_code.is_expired():
            reset_code.delete()
            return Response({'error': 'el codigo de verificacion ya vencio'}, status=403)
        
        return Response({'message':'codigo valido'}, status=200)
    except Exception as e:
        return Response({'error':f'{e}'}, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.filter(email=email).first()
        reset_code = PasswordResetCode.objects.filter(user = user).first()
        if not new_password:
            return Response({'error': 'envia la contrasena nueva'}, status=400)

        if user:
            user.set_password(new_password)
            user.save()

            reset_code.delete()

            request.user.auth_token.delete()

            return Response({'message':'La contrasena ha sido actualizada con exito'})
        else:
            return Response({'error':'El usuario no existe'})
    except Exception as e:
        return Response({'error': e }, status=500)


