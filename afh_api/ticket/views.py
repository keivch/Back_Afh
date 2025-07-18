from .Serializer import TicketSerializer
from .models import Ticket
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from tool.models import Tool
import pytz
from django.contrib.auth.models import User
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from .Services import createTicket, sendMail, changeStateFunction, pdfCreator

# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTicket(request):
    data = request.data
    # Zona horaria de Colombia
    zona_colombia = pytz.timezone('America/Bogota')

    try:
        tools_ids = data.get('tools', [])
        tools = Tool.objects.filter(id__in = tools_ids)
        description = data.get('description')
        applicant_email = data.get('email')
        place = data.get('place')
        responsible = data.get('responsible')
        
        newTicket = createTicket(applicant_email, tools, description, place, responsible)

        fecha_colombia = newTicket.entry_date.astimezone(zona_colombia)

        sendMail(fecha_colombia, newTicket.place)

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
@permission_classes([IsAuthenticated])
def changeState(request):
    data = request.data

    try:
        state= data.get('status')
        id = data.get('id')

        changeStateFunction(id, state)

        return Response({'message': 'estado del ticket actualizado correctamente'})
    except Exception as e:
        return  Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def createPdfTicket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id = ticket_id)

        template = get_template('ticket/solicitud.html')

        buffer = pdfCreator(ticket, 1)

        # Preparar respuesta como archivo descargable
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="solicitud{ticket.place}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def getInforme(request):
    try:
        
        buffer = pdfCreator(None, 2)

        # Preparar respuesta como archivo descargable
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="informe.pdf"'
        return response
    except Exception as e:
        print(str(e))
        return Response({'error': str(e)}, status=500)