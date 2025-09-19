from rest_framework import serializers
from .models import Account, Egress, Income

class AccountSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    initial_amount_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'initial_amount',
            'initial_amount_formatted',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_initial_amount_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.initial_amount).replace(",", ".")
        except Exception as e:
            print(f"Error formatting initial amount: {e}")
            return str(obj.initial_amount)

class EgressSerializer(serializers.ModelSerializer):
    amount_formatted = serializers.SerializerMethodField()
    origin_account_info = AccountSerializer(source='origin_account', read_only=True)
    
    class Meta:
        model = Egress
        fields = [
            'id',
            'responsible',
            'amount',
            'amount_formatted',
            'date',
            'reason',
            'payment_method',
            'observations',
            'voucher',
            'origin_account',
            'origin_account_info'
        ]
    
    def get_amount_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.amount).replace(",", ".")
        except Exception as e:
            print(f"Error formatting amount: {e}")
            return str(obj.amount)
class IncomeSerializer(serializers.ModelSerializer):
    amount_formatted = serializers.SerializerMethodField()
    destination_account_info = AccountSerializer(source='destination_account', read_only=True)
    
    class Meta:
        model = Income
        fields = [
            'id',
            'responsible',
            'amount',
            'amount_formatted',
            'date',
            'reason',
            'payment_method',
            'observations',
            'voucher',
            'destination_account',
            'destination_account_info'
        ]
    
    def get_amount_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.amount).replace(",", ".")
        except Exception as e:
            print(f"Error formatting amount: {e}")
            return str(obj.amount)