from .models import Quotes
from Customer.models import Customer
from datetime import datetime
import pytz
from django.template.loader import get_template
import weasyprint
from io import BytesIO
from WorkOrder.models import WorkOrder
from django.conf import settings
from django.core.mail import send_mail
from users.models import Users
from Option.service import update_option
from item.service import update_item
from Option.models import Option
from Option.service import create_option
from .Serializer import QuotesSerializer

YEAR = datetime.now().year
# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
# Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)


def create_quote(customer_id, options, description, tasks):
    try:
        number = Quotes.objects.count() + 1
        code = f"{number}-{YEAR}"
        new_quote = Quotes.objects.create(
            code = code,
            customer = Customer.objects.get(id=customer_id),
            description = description,
            issue_date = HORA_COLOMBIA,
            state = 1,  # PROCESO
            tasks = tasks
        )
        for option in options:
            new_quote.options.add(option)
        new_quote.save()
        return new_quote
    except Exception as e:
        raise Exception(f"Error creating quote: {str(e)}")
    
def update_quote(id, customer_id=None, options=None, description=None, tasks=None):
    try:
        quote = Quotes.objects.get(id=id)
        if customer_id is not None:
            quote.customer = Customer.objects.get(id=customer_id)
        if options is not None:
            quote.options.clear()
            for option in options:
                quote.options.add(option)
        if description is not None:
            for opt in quote.options.all():
                opt.name = description
                opt.save()
            quote.description = description
        if tasks is not None:
            quote.tasks = tasks
        quote.save()
        return quote
    except Exception as e:
        raise Exception(f"Error updating quote: {str(e)}")

def delete_quote(id):
    try:
        quote = Quotes.objects.get(id=id)
        quote.delete()
        return True
    except Quotes.DoesNotExist:
        raise Exception("Quote not found")
    except Exception as e:
        raise Exception(f"Error deleting quote: {str(e)}")
    
def get_quotes():
    try:
        quotes = Quotes.objects.all()
        return quotes
    except Exception as e:
        raise Exception(f"Error retrieving quotes: {str(e)}")
    
def get_quote_by_id(id):
    try:
        quote = Quotes.objects.get(id=id)
        return quote
    except Exception as e:
        raise Exception(f"Error retrieving quote by ID: {str(e)}")
    
def pdf_quote(id_quote):
    try:
        quote = Quotes.objects.get(id=id_quote)
        data = QuotesSerializer(quote).data
        template = get_template('Quote.html')
        html = template.render({
            "code": data['code'],
            "customer": data['customer']['name'],
            "contacto_cliente": data['customer']['email'],
            "descripcion": data['description'],
            "tasks": data['tasks'],
            "opciones": data['options'],
            "fecha": quote.issue_date.strftime("%d/%m/%Y"),
            "logo_url": 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png'
        })

        buffer = BytesIO()
        weasyprint.HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")
    
def change_state_quote(id_quote, state):
    try:
        quote = Quotes.objects.get(id=id_quote)
        if state not in [1, 2, 3]:  # PROCESO, APROBADO, RECHAZADO
            raise ValueError("Invalid state")
        quote.state = state
        quote.save()
        if state == 2:
            WorkOrder.objects.create(
                Quotes=quote,
                start_date=HORA_COLOMBIA,
                end_date=None  # End date can be set later
            )
        
            # Send email notification
            admins = Users.objects.filter(role = 1).all()
            for amdin in admins:
                subject = f"Nueva orden de trabajo generada"
                message = (
                    f"Se ha generado una nueva orden de trabajo para la cotización {quote.code}.\n\n"
                    f"Cliente: {quote.customer.name}\n\n"
                    f"Descripción: {quote.description}\n\n"
                    f"Fecha de emisión: {quote.issue_date.strftime('%d/%m/%Y')}\n\n"
                    f"Atentamente,\n"
                    f"Equipo de Serenity"
                )
                recipient = [amdin.user.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
        return quote
    except Quotes.DoesNotExist:
        raise Exception("Quote not found")
    except Exception as e:
        raise Exception(f"Error changing quote state: {str(e)}")
    

def add_option_to_quote(quote_id, items, description):
    try:
        quote = Quotes.objects.get(id=quote_id)      
        new_option = create_option(description, items) 
        quote.options.add(new_option)
        quote.save()
        return quote
    except Quotes.DoesNotExist:
        raise Exception("Quote not found")
    


    