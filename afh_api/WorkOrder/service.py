from datetime import datetime
import pytz
from .models import WorkOrder
from django.template.loader import get_template
import weasyprint
from io import BytesIO
from .Serializer import WorkOrderSerializer

# Zona horaria de Colombia
ZONA_COLOMBIA = pytz.timezone('America/Bogota')
# Hora actual en Colombia
HORA_COLOMBIA = datetime.now(ZONA_COLOMBIA)


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
            "code": data['Quotes']['code'],
            "customer": data['Quotes']['customer']['name'],
            "contacto_cliente": data['Quotes']['customer']['email'],
            "descripcion": data['Quotes']['description'],
            "tasks": data['Quotes']['tasks'],
            "opcion": data['Quotes']['options'],
            "fecha": work.start_date.strftime("%d/%m/%Y"),
            "logo_url": 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png',
            "iva": data['Quotes']['iva_value'],
            "utility": data['Quotes']['utility_value'],
            "unforeseen": data['Quotes']['unforeseen_value'],
            "administration": data['Quotes']['administration_value'],
            'method_of_payment': data['Quotes']['method_of_payment'],
            "revision": data['Quotes']['revision']

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
