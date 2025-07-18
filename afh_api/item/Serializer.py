from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    unit_value_formatted = serializers.SerializerMethodField()
    total_value_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id',
            'description',
            'units',
            'amount',
            'unit_value',
            'total_value',
            'unit_value_formatted',
            'total_value_formatted',
        ]

    def get_unit_value_formatted(self, obj):
        return self.format_currency(obj.unit_value)

    def get_total_value_formatted(self, obj):
        return self.format_currency(obj.total_value)

    def format_currency(self, value):
        try:
            return "${:,.0f}".format(value).replace(",", ".")
        except:
            return str(value)
