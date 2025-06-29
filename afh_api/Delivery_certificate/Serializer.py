from rest_framework import serializers
from .models import Delivery_certificate
from exhibit.Serializer import ExhibitSerializer
from WorkOrder.Serializer import WorkOrderSerializer

class DeliveryCertificateSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer(read_only=True)
    exhibit = ExhibitSerializer(many=True, read_only=True)
    class Meta:
        model = Delivery_certificate
        fields = '__all__'