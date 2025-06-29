from rest_framework import serializers
from .models import WorkOrder
from Quotes.Serializer import QuotesSerializer

class WorkOrderSerializer(serializers.ModelSerializer):
    quote = QuotesSerializer()
    class Meta:
        model = WorkOrder
        fields = '__all__'
