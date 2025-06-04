from rest_framework import serializers
from .models import Option
from item.Serializer import ItemSerializer

class OptionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Option
        fields = '__all__'
        