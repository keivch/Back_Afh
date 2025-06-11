from rest_framework import serializers
from .models import Option
from item.Serializer import ItemSerializer
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

class OptionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    total_value_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = [
            'id',
            'name',
            'total_value',
            'total_value_formatted',
            'items'
        ]
    
    def get_total_value_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.total_value).replace(",", ".")
        except:
            return str(obj.total_value)
        