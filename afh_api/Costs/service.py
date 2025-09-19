from math import e
from .models import Costs
from WorkOrder.models import WorkOrder
from Option.models import Option
from django.template.loader import get_template
from io import BytesIO
import weasyprint
from .serializer import CostsSerializer
from babel.dates import format_date

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

def generate_pdf(cost_id):
    try:
        cost = Costs.objects.get(id=cost_id)
        template = get_template('pdfCosts.html')
        data = CostsSerializer(cost).data
        
        # Calcular la diferencia entre costos y total de la orden de trabajo
        costos_total = float(data['items']['subtotal_numeric'])
        orden_total = float(cost.work_order.quote.total_value)
        diferencia = costos_total - orden_total
        
        # Formatear la diferencia como moneda
        diferencia_absoluta = abs(diferencia)
        diferencia_formateada = "${:,.0f}".format(diferencia_absoluta).replace(",", ".")
        
        html = template.render({
            'cost': cost,
            'opcion': data['items'],
            'diferencia': diferencia,
            'diferencia_formateada': diferencia_formateada,
            'orden_total': orden_total,
            'costos_total': costos_total,
            'logo_url': 'https://res.cloudinary.com/dp4tvthea/image/upload/v1756313054/afhlogoazul_rxcpcv.png',
            'fecha': format_date(cost.work_order.quote.issue_date, "d 'de' MMMM 'de' y", locale="es"),
            'total_orden': data['work_order']['quote']['total_value_formatted']
        })
        buffer = BytesIO()
        weasyprint.HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        raise e