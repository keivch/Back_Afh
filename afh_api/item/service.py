from .models import Item
from Option.models import Option
from Quotes.models import Quotes


def create_item(description, units, amount, unit_value):
    try:
        total_value = amount * unit_value
        item = Item.objects.create(
            description=description,
            units=units,
            amount=amount,
            unit_value=unit_value,
            total_value=total_value
        )
        return item
    except Exception as e:
        raise Exception(f"Error creating item: {str(e)}")
    
def update_item(id, description=None, units=None, amount=None, unit_value=None):
    try:
        item = Item.objects.get(id=id)
        print(amount)
        if description is not None:
            item.description = description
        if units is not None:
            item.units = units
        if amount is not None:
            item.amount = amount
            item.save()
        if unit_value is not None or amount is not None:
            item.unit_value = unit_value
            item.total_value = item.amount * unit_value 
        item.save()
        options = Option.objects.filter(items__in=[item]).first()
        if  options:
            subtotal = 0
            for item in options.items.all():
                subtotal += item.total_value
            options.subtotal = subtotal
            options.save()
        if Quotes.objects.filter(options = options).exists():
            quote = Quotes.objects.get(options=options)
            quote.administration_value = options.subtotal * quote.administration
            quote.utility_value = options.subtotal * quote.utility
            quote.unforeseen_value = options.subtotal * quote.unforeseen
            quote.options.total_value = options.subtotal + quote.iva_value + quote.utility_value + quote.unforeseen_value + quote.administration_value
            quote.options.save()
            quote.iva_value = quote.administration_value * quote.iva
            quote.save()
        return item
    except Exception as e:
        raise Exception(f"Error updating item: {str(e)}")

def delete_item(id):
    try:
        item = Item.objects.get(id=id)
        item.delete()
        return True
    except Item.DoesNotExist:
        raise Exception("Item not found")
    except Exception as e:
        raise Exception(f"Error deleting item: {str(e)}")
    
def get_items():
    try:
        items = Item.objects.all()
        return items
    except Exception as e:
        raise Exception(f"Error retrieving items: {str(e)}")
    
def get_item_by_id(id):
    try:
        item = Item.objects.get(id=id)
        return item
    except Exception as e:
        raise Exception(f"Error retrieving item by ID: {str(e)}")
    
