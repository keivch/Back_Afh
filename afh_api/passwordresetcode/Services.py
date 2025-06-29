from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import PasswordResetCode

def sendMailRecovery(email, user):
    
    code = get_random_string(4, '0123456789')  

    # Guardar el código en la BD
    PasswordResetCode.objects.create(user=user, code=code)

    # Enviar el código por correo
    subject = "Codigo de recuperacion"
    message = (
            f"Hola {user.first_name},\n\n"
            f"A continuacion te enviamos tu codigo para restablecer tu contrasena (tiene un tiempo de duracion de 20 minutos)\n\n"
            f"Codigo: {code}\n\n"
            f"Atentamente,\n"
            f"Equipo de Serenity"
        )
        
    recipient = [user.email]

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
    