from django.shortcuts import render
from .Serializer import TicketSerializer
from .models import Ticket
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from tool.models import Tool
from users.models import  Users
from datetime import datetime
import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


@api_view(['POST'])
def addTicket(request):
    data = request.data
        # Zona horaria de Colombia
    zona_colombia = pytz.timezone('America/Bogota')
    # Hora actual en Colombia
    hora_colombia = datetime.now(zona_colombia)
    try:
        tools_ids = data.get('tools', [])
        tools = Tool.objects.filter(id__in = tools_ids)
        description = data.get('description')
        applicant_email = data.get('email')
        receiver = Users.objects.filter(role = 1).first()
        place = data.get('place')
        entry_date = hora_colombia

        if not tools_ids or not description or not applicant_email or not place:
            return Response({'error':'Faltan datos'}, status=400)
        
        user = User.objects.filter(email = applicant_email).first()
        applicant = Users.objects.filter(user = user).first()
        
        newTicket = Ticket.objects.create(
            description = description,
            applicant = applicant,
            receiver = receiver,
            place = place,
            entry_date = entry_date,
            departure_date = None
        )

        newTicket.tools.add(*tools)

        # Enviar el código por correo
        subject = "Codigo de recuperacion"
        message = (
                f"Hola {receiver.user.first_name},\n\n"
                f"Tienes una nueva solicitud de retiro de herramientas en el sistema\n\n"
                f"Lugar de trabajo: {place}\n\n"
                f"fecha de solicitud {entry_date}\n\n"
                f"Atentamente,\n"
                f"Equipo de Serenity"
            )
        
        recipient = [receiver.user.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)

        return Response({'message': 'Ticket creado con exito'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
def getTickets(request):
    try:
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many = True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def changeState(request):
    data = request.data

    try:
        state= data.get('status')
        id = data.get('id')

        ticket = Ticket.objects.get(id = id)

        ticket.state = int(state)
        ticket.save()

        return Response({'message': 'estado del ticket actualizado correctamente'})
    except Exception as e:
        return  Response({'error': str(e)}, status=500)
        

