from .models import WorkAdvance
from exhibit.models import Exhibit

def add_work_advance(exhibits_ids, description, date):
    """
    Create a new WorkAdvance instance and associate it with the given exhibits.
    
    :param exhibits_ids: List of exhibit IDs to associate with the WorkAdvance.
    :param description: Description of the WorkAdvance.
    :param date: Date of the WorkAdvance.
    :return: The created WorkAdvance instance.
    """
    try:
        work_advance = WorkAdvance.objects.create(description=description, date=date)
        for exhibit_id in exhibits_ids:
            exhibit = Exhibit.objects.get(id=exhibit_id)
            work_advance.exhibits.add(exhibit)
        return work_advance
    except Exception as e:
        print(f"Error creating WorkAdvance: {e}")
        return None
    
def edit_work_advance(work_advance_id, exhibits_ids=None, description=None, date=None):
    """
    Edit a new WorkAdvance instance and associate it with the given exhibits.
    
    :param exhibits_ids: List of exhibit IDs to associate with the WorkAdvance.
    :param description: Description of the WorkAdvance.
    :param date: Date of the WorkAdvance.
    :return: Work advance edited.
    """
    try:
        work_advance = WorkAdvance.objects.get(id=work_advance_id)
        if exhibits_ids is not None:
            work_advance.exhibits.clear()
            for exhibit_id in exhibits_ids:
                exhibit = Exhibit.objects.get(id=exhibit_id)
                work_advance.exhibits.add(exhibit)
        if description is not None:
            work_advance.description = description
        if date is not None:
            work_advance.date = date
        work_advance.save()
        return work_advance
    except Exception as e:
        print(f"Error editing WorkAdvance: {e}")
        return None

def get_work_advance():
    """
    get all work advances.
    
    :return: List of all work advances.
    """
    try:
        return WorkAdvance.objects.all()
    except Exception as e:
        print(f"Error retrieving WorkAdvances: {e}")
        return None

def delete_work_advance(work_advance_id):
    """
    Delete a work advance by id.
    :param work_advance_id: ID of the WorkAdvance to delete.
    :return: True if deleted, False otherwise.
    """

    try:
        work = WorkAdvance.objects.get(id=work_advance_id)
        work.delete()
        return True
    except WorkAdvance.DoesNotExist:
        print(f"WorkAdvance with id {work_advance_id} does not exist.")
        return False
    
def get_work_advance_by_id(work_advance_id):
    """
    Get a work advance by id.
    :param id: Id of the work advance.
    :return: Work advance instance or None
    """

    try:
        return WorkAdvance.objects.get(id=work_advance_id)
    except WorkAdvance.DoesNotExist:
        print(f"WorkAdvance with id {work_advance_id} does not exist.")
        return None