from rest_framework import serializers
from .models import Maintenance
from tool.Serializer import ToolSerializer

class MaintenanceSerializer(serializers.ModelSerializer):
    tool = ToolSerializer()
    class Meta:
        model = Maintenance
        fields = '__all__'