from .models import WorkProgress
from WorkAdvance.models import WorkAdvance
from Customer.models import Customer

def add_advance_to_progress(work_progress_id, work_advance_id):
    try:
        work_progress = WorkProgress.objects.get(id=work_progress_id)
        work_advance = WorkAdvance.objects.get(id=work_advance_id)
        work_progress.work_advance.add(work_advance)
        work_progress.save()
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
        work_progress.status = new_status
        work_progress.save()
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