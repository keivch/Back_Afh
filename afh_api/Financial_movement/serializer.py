from rest_framework import serializers
from .models import Egress, Income

class EgressSerializer(serializers.ModelSerializer):
    amount_formatted = serializers.SerializerMethodField()
    class Meta:
        model = Egress
        fields = [
            'id',
            'responsible',
            'amount',
            'date',
            'reason',
            'payment_method',
            'observations',
            'voucher',
            'origin_account',
            'amount_formatted'
        ]
    def get_amount_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.amount).replace(",", ".")
        except:
            return str(obj.amount)
class IncomeSerializer(serializers.ModelSerializer):
    amount_formatted = serializers.SerializerMethodField()
    class Meta:
        model = Income
        fields =  [
            'id',
            'responsible',
            'amount',
            'date',
            'reason',
            'payment_method',
            'observations',
            'voucher',
            'destination_account',
            'amount_formatted'
        ]
    def get_amount_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.amount).replace(",", ".")
        except:
            return str(obj.amount)