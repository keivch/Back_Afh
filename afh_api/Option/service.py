from .models import Option

def create_option(name, items):
    try:
        newOption = Option.objects.create(name=name, total_value=0)
        total_value = 0
        for item in items:
            newOption.items.add(item)
            total_value += item.total_value
        newOption.total_value = total_value
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
            option.total_value = total_value
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
