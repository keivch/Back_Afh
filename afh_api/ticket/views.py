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
from django.contrib.auth.models import User
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from Services import createTicket, sendMail, changeStateFunction

# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


@api_view(['POST'])
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
        
        newTicket = createTicket(applicant_email, tools, description, place)

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

        zona_colombia = pytz.timezone('America/Bogota')

        fecha_colombia = ticket.entry_date.astimezone(zona_colombia)
        

        html = None

        if ticket.state == 3:
            html = template.render({
            'titulo': "Solicitud de Herramienta",
            'solicitante': f"{ticket.applicant.user.first_name} {ticket.applicant.user.last_name}",
            'receptor': f"{ticket.receiver.user.first_name} {ticket.receiver.user.last_name}",
            'fecha_solicitud': fecha_colombia.strftime("%d/%m/%Y %H:%M:%S"),
            'descripcion': ticket.description,
            'lugar': ticket.place,
            'herramientas': ticket.tools.all(),
            'logo_url': 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png'

    })
        if ticket.state == 4:
            fecha_salida = ticket.departure_date.astimezone(zona_colombia)
            html = template.render({
            'titulo': "Entrega de Herramienta",
            'solicitante': f"{ticket.applicant.user.first_name} {ticket.applicant.user.last_name}",
            'receptor': f"{ticket.receiver.user.first_name} {ticket.receiver.user.last_name}",
            'fecha_solicitud': fecha_colombia.strftime("%d/%m/%Y %H:%M:%S"),
            'fecha_entrega': fecha_salida.strftime("%d/%m/%Y %H:%M:%S"),
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

@api_view(['GET'])
def getInforme(request):
    try:
        toolsInUse = Ticket.objects.filter().all()
        totalToolsInUse = Tool.objects.filter(state = 3).all()
        toolsActive = Tool.objects.filter(state=1).all()
        toolsInactive = Tool.objects.filter(state = 2).all() 
        toolsReserve = Tool.objects.filter(state = 4).all()      
        totalTools = Tool.objects.all().count()

        toolsInUseWithPlace = []
        seen_codes = set()
        toolsInReserve = []

        for ticket in toolsInUse:
            for tool in ticket.tools.all():
                if tool.code not in seen_codes and tool.state == 3 and ticket.state == 1:
                    toolsInUseWithPlace.append({
                        'name': tool.name,
                        'code': tool.code,
                        'place': ticket.place
                    })
                    seen_codes.add(tool.code)
                if tool.code not in seen_codes and tool.state == 4 and ticket.state == 3:
                    toolsInReserve.append({
                        'name': tool.name,
                        'code': tool.code
                    })
                    seen_codes.add(tool.code)

        zona_colombia = pytz.timezone('America/Bogota')
        
        template = get_template('ticket/informe.html')


        html = template.render({
            'fecha_generacion': datetime.now(zona_colombia).strftime("%d/%m/%Y %H:%M:%S"),
            'total_herramientas': totalTools,
            'total_activas': toolsActive.count(),
            'total_inactivas': toolsInactive.count(),
            'total_en_uso': totalToolsInUse.count(),
            'total_en_reserva': toolsReserve.count(),
            'herramientas_activas': toolsActive,
            'herramientas_inactivas': toolsInactive,
            'herramientas_en_uso': toolsInUseWithPlace,
            'herramientas_en_reserva': toolsInReserve,
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
        response['Content-Disposition'] = f'attachment; filename="informe.pdf"'
        return response
    except Exception as e:
        print(str(e))
        return Response({'error': str(e)}, status=500)