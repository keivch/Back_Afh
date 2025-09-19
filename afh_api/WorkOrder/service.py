from datetime import datetime
import pytz
from .models import WorkOrder
from django.template.loader import get_template
import weasyprint
from io import BytesIO
from .Serializer import WorkOrderSerializer
from Quotes.models import Quotes
from Delivery_certificate.models import Delivery_certificate
from WorkProgress.models import WorkProgress
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from babel.dates import format_date
from Costs.models import Costs

# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
# Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)

def send_email(customer, code):
    try:
        subject = "Bienvenido al portal para clientes de AFH"
        recipient = customer.email

        context={
        'nombre': customer.name,
        'link': 'http://localhost:4200/login-customer',
        'code': code
    }

        html_content = render_to_string('email.html', context)
        text_content = strip_tags(html_content)

        new_email  = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [recipient]
        )
        new_email.attach_alternative(html_content, "text/html")
        new_email.send()
    except Exception as e:
        print(str(e))

def create_work_order(quote_id, start_date, days_of_execution, description, workplace, number_technicians, number_officers, number_auxiliaries, activity, permissions, number_supervisors):
    try:
        quote = Quotes.objects.get(id=quote_id)

        new_work_order = WorkOrder(
            quote = quote,
            start_date = start_date,
            description = description,
            workplace = workplace,
            number_technicians = number_technicians,
            number_officers = number_officers,
            number_auxiliaries = number_auxiliaries,
            activity = activity,
            permissions = permissions,
            number_supervisors = number_supervisors,
            days_of_execution = days_of_execution
        )
        new_work_order.save()
        #creacion del progreso de trabajo
        WorkProgress.objects.create(work_order = new_work_order)
        #enviar correo al cliente
        send_email(quote.customer, quote.code)
        
        return new_work_order
    except Exception as e:
        raise Exception(f"Error creating work order: {str(e)}")
    
def update_work_order(id, quote_id = None,  start_date = None, days_of_execution = None, description = None, workplace = None, number_technicians = None, number_officers = None, number_auxiliaries = None, activity = None, permissions = None, number_supervisors = None):
    try:
        work_order = WorkOrder.objects.get(id=id)
        if quote_id is not None:
            work_order.quote = Quotes.objects.get(id=quote_id)
        if start_date is not None:
            work_order.start_date = start_date
        if description is not None:
            work_order.description = description
        if workplace is not None:
            work_order.workplace = workplace
        if number_technicians is not None:
            work_order.number_technicians = number_technicians
        if number_officers is not None:
            work_order.number_officers = number_officers
        if number_auxiliaries is not None:
            work_order.number_auxiliaries = number_auxiliaries
        if activity is not None:
            work_order.activity = activity
        if permissions is not None:
            work_order.permissions = permissions
        if number_supervisors is not None:
            work_order.number_supervisors = number_supervisors
        if days_of_execution is not None:
            work_order.days_of_execution = days_of_execution
        work_order.save()
        return work_order
    except Exception as e:
        raise Exception(f"Error updating work order: {str(e)}")


def get_work_orders():
    try:
        work_orders = WorkOrder.objects.all()
        return work_orders
    except Exception as e:
        raise Exception(f"Error retrieving work orders: {str(e)}")
    
def get_work_order_by_id(id):
    try:
        work_order  = WorkOrder.objects.get(id=id)
        return work_order
    except WorkOrder.DoesNotExist:
        raise Exception("Work order not found")
    
def create_pdf(id):
    try:
        work = WorkOrder.objects.get(id=id)
        data = WorkOrderSerializer(work).data
        template = get_template('workorder.html')
        html = template.render({
            "code": data['quote']['code'],
            "customer": data['quote']['customer']['name'],
            "contacto_cliente": data['quote']['customer']['email'],
            "descripcion": data['quote']['description'],
            "tasks": data['quote']['tasks'],
            "opcion": data['quote']['options'],
            "fecha": format_date(work.start_date, "d 'de' MMMM 'de' y", locale="es"),
            "logo_url": 'https://res.cloudinary.com/dp4tvthea/image/upload/v1756313054/afhlogoazul_rxcpcv.png',
            "iva": data['quote']['iva_value'],
            "utility": data['quote']['utility_value'],
            "unforeseen": data['quote']['unforeseen_value'],
            "administration": data['quote']['administration_value'],
            'method_of_payment': data['quote']['method_of_payment'],
            "revision": data['quote']['revision'],
            "start_date": work.start_date.strftime("%d/%m/%Y"),
            "end_date": work.end_date.strftime("%d/%m/%Y") if work.end_date else "N/A",
            "description": work.description,
            "workplace": work.workplace,
            "number_technicians": work.number_technicians,
            "number_officers": work.number_officers,
            "number_auxiliaries": work.number_auxiliaries,
            "number_supervisors": work.number_supervisors,
            "activity": work.activity,
            "permissions": work.permissions if work.permissions else {}

        })

        buffer = BytesIO()
        weasyprint.HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")
    
def finish_work(id):
    try:
        work = WorkOrder.objects.get(id=id)
        work.end_date = HORA_COLOMBIA
        work.save()
        return True
    except WorkOrder.DoesNotExist:
        raise Exception("Work order not found")
    
def get_work_order_whitout_certificate():
    try:
        works = WorkOrder.objects.filter().exclude(id__in = Delivery_certificate.objects.values_list('work_order_id', flat=True))
        return works
    except Exception as e:
        raise Exception(f"Error retrieving work orders without delivery certificate: {str(e)}")

def get_work_order_whitout_costs():
    try:
        works = WorkOrder.objects.filter().exclude(id__in = Costs.objects.values_list('work_order_id', flat=True))
        return works
    except Exception as e:
        raise Exception(f"Error retrieving work orders without costs: {str(e)}")
