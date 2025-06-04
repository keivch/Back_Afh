from rest_framework import serializers
from .models import Quotes
from Customer.Serializer import ClienteSerializer
from Option.Serializer import OptionSerializer



class QuotesSerializer(serializers.ModelSerializer):
    customer = ClienteSerializer()
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Quotes
        fields = '__all__'