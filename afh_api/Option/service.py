from .models import Option
from item.models import Item
from item.service import create_item
from Quotes.models import Quotes

def create_option(name, items_ids):
    try:
        newOption = Option.objects.create(name=name, total_value=0)
        items = Item.objects.filter(id__in=items_ids)
        sub_total = 0
        for item in items:
            newOption.items.add(item)
            sub_total += item.total_value
        newOption.subtotal = sub_total
        newOption.save()
        return newOption
    except Exception as e:
        raise Exception(f"Error creating option: {str(e)}")
    
def update_option(id, name=None, items=None):
    try:
        option = Option.objects.get(id=id)
        if name is not None:
            option.name = name
        if items is not None:
            option.items.clear()
            total_value = 0
            for item in items:
                option.items.add(item)
                total_value += item.total_value
            option.subtotal = total_value
        option.save()
        return option
    except Exception as e:
        raise Exception(f"Error updating option: {str(e)}")
    
def delete_option(id):
    try:
        option = Option.objects.get(id=id)
        option.delete()
        return True
    except Option.DoesNotExist:
        raise Exception("Option not found")
    except Exception as e:
        raise Exception(f"Error deleting option: {str(e)}")

def get_options():
    try:
        options = Option.objects.all()
        return options
    except Exception as e:
        raise Exception(f"Error retrieving options: {str(e)}")
    
def get_option_by_id(id):
    try:
        option = Option.objects.get(id=id)
        return option
    except Exception as e:
        raise Exception(f"Error retrieving option by ID: {str(e)}")
    
def add_item_to_option(option_id, items):
    try:
        option = Option.objects.get(id=option_id)
        sub_total = option.subtotal
        for item in items:
            new_item = create_item(item['description'], item['units'], item['amount'], item['unit_value'])  
            option.items.add(new_item)
            sub_total += new_item.total_value
        option.subtotal = sub_total
        if Quotes.objects.get(options=option):
            quote = Quotes.objects.get(options=option)
            if quote.construction is not None:                
                quote.iva_value = sub_total * quote.iva
                quote.utility_value = sub_total * quote.utility
                quote.unforeseen_value = sub_total * quote.unforeseen
                quote.administration_value = sub_total * quote.administration
                total_value = sub_total + quote.iva_value + quote.utility_value + quote.unforeseen_value + quote.administration_value
                option.total_value = total_value
            else:
                quote.iva_value = sub_total * quote.iva
                total_value = sub_total + quote.iva_value
                option.total_value = total_value
            quote.save()
        option.save()
        return option
    except Option.DoesNotExist:
        raise Exception("Option not found")
