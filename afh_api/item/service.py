from .models import Item
from Option.models import Option
from Quotes.models import Quotes


def create_item(description, units, amount, unit_value):
    try:
        item = Item.objects.create(
            description=description,
            units=units,
            amount=amount,
            unit_value=unit_value,
        )
        return item
    except Exception as e:
        raise Exception(f"Error creating item: {str(e)}")
    
def update_item(id, description=None, units=None, amount=None, unit_value=None):
    try:
        item = Item.objects.get(id=id)
        if description is not None:
            item.description = description
        if units is not None:
            item.units = units
        if unit_value is not None:
            item.unit_value = unit_value
        if amount is not None:
            item.amount = amount
        item.save()
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
    
