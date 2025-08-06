from rest_framework import serializers
from .models import WorkProgress
from WorkAdvance.serializer import WorkAdvanceSerializer
from WorkOrder.Serializer import WorkOrderSerializer

class WorkProgressSerializer(serializers.ModelSerializer):
    work_advance = WorkAdvanceSerializer(many=True, read_only=True)
    work_order = WorkOrderSerializer(read_only=True)

    class Meta:
        model = WorkProgress
        fields = '__all__'