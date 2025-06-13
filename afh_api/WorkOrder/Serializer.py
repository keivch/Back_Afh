from rest_framework import serializers
from .models import WorkOrder
from Quotes.Serializer import QuotesSerializer

class WorkOrderSerializer(serializers.ModelSerializer):
    Quotes = QuotesSerializer()
    class Meta:
        model = WorkOrder
        fields = '__all__'
