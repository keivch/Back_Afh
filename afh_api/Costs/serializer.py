from rest_framework import serializers
from .models import Costs
from Option.Serializer import OptionSerializer
from WorkOrder.Serializer import WorkOrderSerializer

class CostsSerializer(serializers.ModelSerializer):
    items = OptionSerializer()
    work_order = WorkOrderSerializer()
    get_total_value_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Costs
        fields = [
            'id',
            'items',
            'work_order',
            'total_value'
        ]

    def get_total_value_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.total_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting subtotal: {e}")
            return str(obj.total_value)