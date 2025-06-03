from rest_framework import serializers
from .models import Quotes
from Customer.Serializer import ClienteSerializer



class QuotesSerializer(serializers.ModelSerializer):
    customer = ClienteSerializer()
    class Meta:
        model = Quotes
        fields = '__all__'