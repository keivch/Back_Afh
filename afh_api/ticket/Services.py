from users.models import  Users
from django.contrib.auth.models import User
from .models import Ticket
import pytz
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from tool.models import Tool

# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
    # Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)

def createTicket(applicant_email, tools, description, place, responsible):
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
        departure_date = None,
        responsible = responsible
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

def pdfCreator(ticket, type):
    template = None
    if type == 1:
        template = get_template('ticket/solicitud.html')
        fecha_colombia = ticket.entry_date.astimezone(ZONA_COLOMBIA)
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
            'logo_url': 'https://res.cloudinary.com/dp4tvthea/image/upload/v1756313054/afhlogoazul_rxcpcv.png',
            'responsible': ticket.responsible

    })
        if ticket.state == 4:
            fecha_salida = ticket.departure_date.astimezone(ZONA_COLOMBIA)
            html = template.render({
            'titulo': "Entrega de Herramienta",
            'solicitante': f"{ticket.applicant.user.first_name} {ticket.applicant.user.last_name}",
            'receptor': f"{ticket.receiver.user.first_name} {ticket.receiver.user.last_name}",
            'fecha_solicitud': fecha_colombia.strftime("%d/%m/%Y %H:%M:%S"),
            'fecha_entrega': fecha_salida.strftime("%d/%m/%Y %H:%M:%S"),
            'descripcion': ticket.description,
            'lugar': ticket.place,
            'herramientas': ticket.tools.all(),
            'logo_url': 'https://res.cloudinary.com/dp4tvthea/image/upload/v1756313054/afhlogoazul_rxcpcv.png',
            'responsible': ticket.responsible
        })
         # Crear el PDF
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=buffer)
        buffer.seek(0)
        if pisa_status.err:
            return None, 'Error generando el PDF'
        return buffer
    elif type == 2:
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
        
        template = get_template('ticket/informe.html')


        html = template.render({
            'fecha_generacion': datetime.now(ZONA_COLOMBIA).strftime("%d/%m/%Y %H:%M:%S"),
            'total_herramientas': totalTools,
            'total_activas': toolsActive.count(),
            'total_inactivas': toolsInactive.count(),
            'total_en_uso': totalToolsInUse.count(),
            'total_en_reserva': toolsReserve.count(),
            'herramientas_activas': toolsActive,
            'herramientas_inactivas': toolsInactive,
            'herramientas_en_uso': toolsInUseWithPlace,
            'herramientas_en_reserva': toolsInReserve,
            'logo_url': 'https://res.cloudinary.com/dp4tvthea/image/upload/v1756313054/afhlogoazul_rxcpcv.png'
        })

        
         # Crear el PDF
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if pisa_status.err:
            return None, 'Error generando el PDF'

        buffer.seek(0)
        return buffer     
    


        
     
