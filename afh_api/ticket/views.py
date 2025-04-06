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
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
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
    
@api_view(['GET'])
def gtTicketById(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id = ticket_id)
        serializer = TicketSerializer(ticket)
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
    
@api_view(['GET'])
def createPdfTicket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id = ticket_id)

        template = get_template('ticket/solicitud.html')

        html = template.render({
        'solicitante': ticket.applicant.user.first_name,
        'receptor': ticket.receiver.user.first_name,
        'fecha': ticket.entry_date.strftime("%d/%m/%Y %H:%M:%S"),
        'descripcion': ticket.description,
        'lugar': ticket.place,
        'herramientas': ticket.tools.all(),
        'logo_url': 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png'

    })
         # Crear el PDF
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if pisa_status.err:
            return HttpResponse({'error': 'Error generando el PDF'}, status=500)

        buffer.seek(0)

        # Preparar respuesta como archivo descargable
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="solicitud{ticket.place}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)

        

