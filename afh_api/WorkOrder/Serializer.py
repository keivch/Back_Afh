from rest_framework import serializers
from .models import WorkOrder
from Quotes.Serializer import QuotesSerializer

class WorkOrderSerializer(serializers.ModelSerializer):
    quote = QuotesSerializer()
    class Meta:
        model = WorkOrder
        fields = [
            'id',
            'quote',
            'start_date',
            'end_date',
            'description',
            'workplace',
            'number_technicians',
            'number_officers',
            'number_auxiliaries',
            'activity',
            'permissions',
            'number_supervisors',
            'days_of_execution'
        ]
