from .models import Delivery_certificate
from WorkOrder.models import WorkOrder
from exhibit.models import Exhibit
import weasyprint
from io import BytesIO
from django.template.loader import get_template

def create_delivery_certificarte(work_order_id, osbervations, recommendations, exhibit_ids, description, development):
    try:
        work = WorkOrder.objects.get(id=work_order_id)
        exhibits = Exhibit.objects.filter(id__in=exhibit_ids)
        delivery_certificate = Delivery_certificate.objects.create(
            work_order=work,
            observations=osbervations,
            recommendations=recommendations,
            description=description,
            development=development
        )

        for exhibit in exhibits:
            delivery_certificate.exhibit.add(exhibit)
        delivery_certificate.save()

        return delivery_certificate
    except Exception as e:
        print(f"Error creating delivery certificate: {str(e)}")
        return None
    
def update_delivery_certificate(id, observations = None, recommendations = None, description = None, development = None):
    try:
        delivery_certificate = Delivery_certificate.objects.get(id=id)
        if observations is not None:
            delivery_certificate.observations = observations
        if recommendations is not None:
            delivery_certificate.recommendations = recommendations
        if description is not None:
            delivery_certificate.description = description
        if development is not None:
            delivery_certificate.development = development
        delivery_certificate.save()
        return delivery_certificate
    except Exception as e:
        print(f"Error updating delivery certificate: {str(e)}")
        return None
    
def get_deliverys_certificates():
    try:
        delivery_certificates = Delivery_certificate.objects.all()
        return delivery_certificates
    except Exception as e:
        print(f"Error retrieving delivery certificates: {str(e)}")
        return None
    
def get_delivery_certificate_by_id(id):
    try:
        delivery_certificate = Delivery_certificate.objects.get(id=id)
        return delivery_certificate
    except Delivery_certificate.DoesNotExist:
        print("Delivery certificate not found")
        return None
    except Exception as e:
        print(f"Error retrieving delivery certificate: {str(e)}")
        return None
    
def add_exhibit_to_delivery_certificate(delivery_certificate_id, exhibit_id):
    try:
        delivery_certificate = Delivery_certificate.objects.get(id=delivery_certificate_id)
        exhibit = Exhibit.objects.get(id=exhibit_id)
        delivery_certificate.exhibit.add(exhibit)
        delivery_certificate.save()
        return delivery_certificate
    except Exception as e:
        print(f"Error adding exhibit to delivery certificate: {str(e)}")
        return None
    
def create_pdf(id):
    try:
        delivery = get_delivery_certificate_by_id(id)
        template = get_template('delivery_certificate.html')
        html = template.render({
            'work_order': delivery.work_order,
            'date': delivery.date.strftime("%d/%m/%Y"),
            'description': delivery.description,
            'development': delivery.development,
            'observations': delivery.observations,
            'recommendations': delivery.recommendations,
            'exhibits': delivery.exhibit.all(),
            'logo_url': 'https://www.afhmetalmecanico.com/wp-glass/wp-content/uploads/2017/04/logoafme3.png'
            })
        
        buffer = BytesIO()
        weasyprint.HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        return None


