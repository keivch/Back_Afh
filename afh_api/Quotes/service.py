from .models import Quotes
from Customer.models import Customer
from datetime import datetime
import pytz

YEAR = datetime.now().year
# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
# Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)


def create_quote(customer_id, options, description, tasks):
    try:
        number = Quotes.objects.count() + 1
        code = f"{YEAR}-{number}"
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
    