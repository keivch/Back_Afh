from users.models import  Users
from django.contrib.auth.models import User
from .models import Ticket
import pytz
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
    # Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)

def createTicket(applicant_email, tools, description, place):
    user = User.objects.filter(email = applicant_email).first()
    applicant = Users.objects.filter(user = user).first()
    receiver = Users.objects.filter(role = 1).first()


    entry_date = HORA_COLOMBIA
        
    newTicket = Ticket.objects.create(
        description = description,
        applicant = applicant,
        receiver = receiver,
        place = place,
        entry_date = entry_date,
        departure_date = None
        )

    for tool in tools:
        tool.state = 4
        tool.save()

    newTicket.tools.add(*tools)

    newTicket.save()

    return newTicket

def sendMail(fecha_colombia, place):
    # Enviar el código por correo
        admins = Users.objects.filter(role = 1).all()
        for admin in admins:
            subject = "Solicitud de retiro Herramienta"
            message = (
                    f"Hola {admin.user.first_name} {admin.user.last_name},\n\n"
                    f"Tienes una nueva solicitud de retiro de herramientas en el sistema\n\n"
                    f"Lugar de trabajo: {place}\n\n"
                    f"fecha y hora de la solicitud {fecha_colombia.strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                    f"Atentamente,\n"
                    f"Equipo de Serenity"
                )
            
            recipient = [admin.user.email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)

def changeStateFunction(id, state):
    ticket = Ticket.objects.get(id = id)

    if int(state) == 1:
        for tool in ticket.tools.all():
            tool.state = 3
            tool.save()

            ticket.state = int(state)
            ticket.save()

    if int(state) == 4:
        
        ticket.departure_date = HORA_COLOMBIA
        for tool in ticket.tools.all():
            tool.state = 1
            tool.save()

        ticket.state = int(state)
        ticket.save()
        
    if int(state) == 2:
        ticket.state = int(state)
        for tool in ticket.tools.all():
            tool.state = 1
            tool.save()
            ticket.tools.remove(tool)

    ticket.save()
        
     
