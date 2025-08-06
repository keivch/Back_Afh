from rest_framework import serializers
from .models import Option
from item.Serializer import ItemSerializer


class OptionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = [
            'id',
            'name',
            'items',
            'subtotal',
        ]
    
    def get_subtotal(self, obj):
        try:
            return "${:,.0f}".format(obj.subtotal).replace(",", ".")
        except Exception as e:
            print(f"Error formatting subtotal: {e}")
            return str(obj.subtotal)
        