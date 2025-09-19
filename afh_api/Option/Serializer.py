from rest_framework import serializers
from .models import Option
from item.Serializer import ItemSerializer


class OptionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    subtotal_numeric = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = [
            'id',
            'name',
            'items',
            'subtotal',
            'subtotal_numeric',
        ]
    
    def get_subtotal(self, obj):
        try:
            return "${:,.0f}".format(obj.subtotal).replace(",", ".")
        except Exception as e:
            print(f"Error formatting subtotal: {e}")
            return str(obj.subtotal)
    
    def get_subtotal_numeric(self, obj):
        try:
            return float(obj.subtotal)
        except Exception as e:
            print(f"Error getting numeric subtotal: {e}")
            return 0.0
        