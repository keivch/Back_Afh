from rest_framework import serializers
from .models import Quotes
from Customer.Serializer import CustomerSerializer
from Option.Serializer import OptionSerializer



class QuotesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    options = OptionSerializer()
    class Meta:
        model = Quotes
        fields = '__all__'