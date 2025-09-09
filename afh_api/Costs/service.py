from math import e
from .models import Costs
from WorkOrder.models import WorkOrder
from Option.models import Option

def create(work_order_id, option_id):
    try:
        work_order = WorkOrder.objects.get(id=work_order_id)
        option = Option.objects.get(id=option_id)
        cost = Costs.objects.create(work_order=work_order, items=option)
        return cost
    except WorkOrder.DoesNotExist:
        return None
    except Option.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error al crear Costs: {e}")
        raise e

def get(cost_id):
    try:
        return Costs.objects.get(id=cost_id)
    except Costs.DoesNotExist:
        raise e

def update(cost_id, work_order_id=None, option_id=None):
    try:
        cost = Costs.objects.get(id=cost_id)
        if work_order_id is not None:
            work_order = WorkOrder.objects.get(id=work_order_id)
            cost.work_order = work_order
        if option_id is not None:
            option = Option.objects.get(id=option_id)
            cost.items = option
        cost.save()
        return cost
    except Costs.DoesNotExist:
        return None
    except WorkOrder.DoesNotExist:
        return None
    except Option.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error al actualizar Costs: {e}")
        raise e

def delete(cost_id):
    try:
        cost = Costs.objects.get(id=cost_id)
        cost.delete()
        return True
    except Costs.DoesNotExist:
        return False
    except Exception as e:
        print(f"Error al eliminar Costs: {e}")
        raise e

def list_all():
    return Costs.objects.all()