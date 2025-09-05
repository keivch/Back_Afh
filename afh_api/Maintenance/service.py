from .models import Maintenance, Tool
from users.models import Users, User
def create(technician_name, tool_id, date, maintenance_days, observations, next_date, type, user_email):
    try:
        if not technician_name or not tool_id or  not date or not maintenance_days or not next_date or not type or not user_email:
            return None
        tool = Tool.objects.get(id=tool_id)
        if not tool:
            return None
        user = User.objects.filter(email = user_email).first()
        user_delivery = Users.objects.filter(user = user).first()
        new_maintenance = Maintenance.objects.create(
            maintenance_technician_name = technician_name,
            tool=tool,
            date = date,
            maintenance_days = maintenance_days,
            observations = observations,
            next_maintenance_date= next_date,
            type = type,
            user_delivery = user_delivery
        )
        
        new_maintenance.change_status_tool()
        return new_maintenance
    except Exception as e:
        raise str(e)
        
def update_maintenance(maintenance_id, technician_name = None, tool_id = None, maintenance_days = None, observations = None, next_date = None, date = None, type = None):
    try:
        maintenance = Maintenance.objects.get(id=maintenance_id)
        if not maintenance:
            return
        if technician_name:
            maintenance.maintenance_technician_name = technician_name
        if tool_id:
            tool = Tool.objects.get(id=tool_id)
            maintenance.tool = tool
        if maintenance_days:
            maintenance.maintenance_days = maintenance_days
        if observations:
            maintenance.observations = observations
        if next_date:
            maintenance.next_maintenance_date = next_date
        if date:
            maintenance.date = date
        if type:
            maintenance.type = type
        maintenance.save()
    except Exception as e:
        raise str(e)

def get_maintenances():
    try:
        maintenances = Maintenance.objects.all()
        return maintenances
    except Exception as e:
        raise str(e)

def get_maintenance_id(maintenance_id):
    try:
        maintenance = Maintenance.objects.get(id = maintenance_id)
        return maintenance
    except Exception as e:
        raise str(e)
