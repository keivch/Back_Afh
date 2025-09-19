from .models import WorkProgress
from WorkAdvance.models import WorkAdvance
from Customer.models import Customer
from service.pusher import pusher_client
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import os


def send_notification(work_progress, tittle, content, type, subject):
    canal_name = str(work_progress.id)
    try:
        pusher_client.trigger(
            canal_name,
            'Nuevo avance registrado',
            {
                'title': tittle,
                'content': content + work_progress.work_order.quote.code
            }
        )

        subject_email = subject + work_progress.work_order.quote.code
        recipient = work_progress.work_order.quote.customer.email
        context = {
            'name_customer': work_progress.work_order.quote.customer.name,
            'code':work_progress.work_order.quote.code
           
        }

        if type == 1:
            html_content = render_to_string('advanceEmail.html', context)
        if type == 2:
            html_content = render_to_string('noti_status.html', context)
        text_content = strip_tags(html_content)

        new_email  = EmailMultiAlternatives(
            subject_email,
            text_content,
            settings.EMAIL_HOST_USER,
            [recipient]
        )
        new_email.attach_alternative(html_content, "text/html")
        
        new_email.send()
    except Exception as e:
        print(str(e))



def add_advance_to_progress(work_progress_id, work_advance_id):
    try:
        work_progress = WorkProgress.objects.get(id=work_progress_id)
        work_advance = WorkAdvance.objects.get(id=work_advance_id)
        work_progress.work_advance.add(work_advance)
        work_progress.save()
        tittle = 'Nuevo avance registrado por afh'
        content = 'Tienes un nuevo avance del trabajo '
        type = 1
        subject = 'Tienes un nuevo avance de tu proyecto '
        send_notification(work_progress=work_progress, tittle=tittle, content=content, subject=subject, type=type)
        return work_progress
    except Exception as e:
        print(f"Error adding advance to progress: {e}")
        return None
    
def remove_advance_from_progress(work_progress_id, work_advance_id):
    try:
        work_progress = WorkProgress.objects.get(id=work_progress_id)
        work_advance = WorkAdvance.objects.get(id=work_advance_id)
        work_progress.work_advance.remove(work_advance)
        work_progress.save()
        return work_progress
    except Exception as e:
        print(f"Error removing advance from progress: {e}")
        return None

def get_work_progress_by_id(work_progress_id):
    try:
        work_progress = WorkProgress.objects.get(id=work_progress_id)
        return work_progress
    except WorkProgress.DoesNotExist:
        print(f"WorkProgress with id {work_progress_id} does not exist.")
        return None
    
def get_all_work_progresses():
    try:
        work_progresses = WorkProgress.objects.all()
        return work_progresses
    except Exception as e:
        print(f"Error retrieving all work progresses: {e}")
        return None

def change_work_progress_status(work_progress_id, new_status):
    try:
        work_progress = WorkProgress.objects.get(id=work_progress_id)
        work_progress.state = new_status
        work_progress.save()
        tittle = 'Tu Trabajo ha cambiado de estado'
        content = 'El estado de tu trabajo ha sido actualizado '
        type = 2
        subject = 'Tu Trabajo ha cambiado de estado '
        send_notification(work_progress=work_progress, tittle=tittle, content=content, subject=subject, type=type)
        return work_progress
    except WorkProgress.DoesNotExist:
        print(f"WorkProgress with id {work_progress_id} does not exist.")
        return None
    except Exception as e:
        print(f"Error changing status of work progress: {e}")
        return None

def validate_customer(code, email):
        customer = Customer.objects.get(email=email)
        work_order = WorkProgress.objects.get(work_order__quote__code=code)
        if work_order and customer:
            return work_order
        else:
            return None

def change_progress_percentage(percentage, work_progress_id):
    try:
        work = WorkProgress.objects.get(id=work_progress_id)
        work.progress_percentage = percentage
        work.save()
    except Exception as e:
        raise e