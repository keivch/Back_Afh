from .models import WorkOrder

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