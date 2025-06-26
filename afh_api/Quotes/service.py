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
from decimal import Decimal

YEAR = datetime.now().year
# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
# Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)


def create_quote(customer_id, options_id, description, tasks, iva, utility, unforeseen, administration, method_of_payment, construction=None):
    try:
        number = Quotes.objects.count() + 1
        code = f"{number}-{YEAR}"

        options = Option.objects.get(id=options_id)

        new_quote = Quotes.objects.create(
            code = code,
            customer = Customer.objects.get(id=customer_id),
            description = description,
            issue_date = HORA_COLOMBIA,
            state = 1,  # PROCESO
            tasks = tasks,
            method_of_payment = method_of_payment,
            options = options,
        )

        if construction is not None:
            utility = Decimal(str(utility))
            unforeseen = Decimal(str(unforeseen))
            administration = Decimal(str(administration))
            iva = Decimal(str(iva))   
            new_quote.iva = iva
            new_quote.utility = utility
            new_quote.unforeseen = unforeseen
            new_quote.administration = administration
            new_quote.construction = construction
        new_quote.save()
        return new_quote
    except Exception as e:
        raise Exception(f"Error creating quote: {str(e)}")
    
def update_quote(id, customer_id=None, description=None, tasks=None, utility=None, unforeseen=None, administration=None, method_of_payment=None, construction=None):
    try:
        quote = Quotes.objects.get(id=id)
        
        if customer_id is not None:
            quote.customer = Customer.objects.get(id=customer_id)
            
        if description is not None:
            quote.options.name = description
            quote.options.save()
            quote.description = description
            
        if tasks is not None:
            quote.tasks = tasks
            
        if construction is not None:
            quote.construction = construction
            
        if utility is not None:
            utility_decimal = Decimal(str(utility))
            quote.utility = utility_decimal

            
        if unforeseen is not None:
            unforeseen_decimal = Decimal(str(unforeseen))
            quote.unforeseen = unforeseen_decimal
            
        if administration is not None:
            administration_decimal = Decimal(str(administration))
            quote.administration = administration_decimal
            
        if method_of_payment is not None:
            quote.method_of_payment = method_of_payment
            
        quote.revision += 1
        quote.options.total_value = quote.options.subtotal + quote.iva_value + quote.utility_value + quote.unforeseen_value + quote.administration_value
        quote.options.save()
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
            "opcion": data['options'],
            "fecha": quote.issue_date.strftime("%d/%m/%Y"),
            "logo_url": 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png',
            "iva": data['iva_value'],
            "utility": data['utility_value'],
            "unforeseen": data['unforeseen_value'],
            "administration": data['administration_value'],
            'method_of_payment': data['method_of_payment'],
            "revision": data['revision'],
            'construction': data['construction'],
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
        return quote
    except Quotes.DoesNotExist:
        raise Exception("Quote not found")
    except Exception as e:
        raise Exception(f"Error changing quote state: {str(e)}")
    

def get_quotes_whitouth_order():
    try:
        quotes = Quotes.objects.filter(state=2).exclude(id__in=WorkOrder.objects.values_list('quote_id', flat=True))
        return quotes
    except Exception as e:
        raise Exception(f"Error retrieving quotes without work orders: {str(e)}")
    
    


    