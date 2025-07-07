from rest_framework import serializers
from .models import Egress, Income

class EgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Egress
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'