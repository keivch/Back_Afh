from rest_framework import serializers
from .models import Maintenance
from tool.Serializer import ToolSerializer
from users.Serializers import UserSerializer

class MaintenanceSerializer(serializers.ModelSerializer):
    tool = ToolSerializer()
    user_delivery = UserSerializer()
    class Meta:
        model = Maintenance
        fields = [
            'id',
            'maintenance_technician_name',
            'tool',
            'date',
            'maintenance_days',
            'observations',
            'next_maintenance_date',
            'type',
            'user_delivery',
            'delivery_date'
        ]