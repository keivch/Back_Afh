from rest_framework import serializers
from .models import Quotes
from Customer.Serializer import CustomerSerializer
from Option.Serializer import OptionSerializer



class QuotesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    options = OptionSerializer()

    iva_value = serializers.SerializerMethodField()
    utility_value = serializers.SerializerMethodField()
    unforeseen_value = serializers.SerializerMethodField()
    administration_value = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()
    total_value_formatted = serializers.SerializerMethodField()
    class Meta:
        model = Quotes
        fields = [
            'id',
            'code',
            'customer',
            'description',
            'issue_date',
            'state',
            'options',
            'tasks',
            'iva',
            'utility',
            'unforeseen',
            'administration',
            'revision',
            'construction',
            'iva_value',
            'utility_value',
            'unforeseen_value',
            'administration_value',
            'method_of_payment',
            'construction',
            'total_value',
            'total_value_formatted',
            'contractor_materials',
            'contracting_materials',
            'delivery_time'
        ]

        

    def get_iva_value(self, obj):
        try:
            return "${:,.0f}".format(obj.iva_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting IVA value: {e}")
            return str(obj.iva_value)
    def get_utility_value(self, obj):
        try:
            return "${:,.0f}".format(obj.utility_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting utility value: {e}")
            return str(obj.utility_value)
    def get_unforeseen_value(self, obj):
        try:
            return "${:,.0f}".format(obj.unforeseen_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting unforeseen value: {e}")
            return str(obj.unforeseen_value)
    def get_administration_value(self, obj):
        try:
            return "${:,.0f}".format(obj.administration_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting administration value: {e}")
            return str(obj.administration_value)
    def get_total_value(self, obj):
        try:
            return "${:,.0f}".format(obj.total_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting total value: {e}")
            return str(obj.total_value)
    
    def get_total_value_formatted(self, obj):
        try:
            return "${:,.0f}".format(obj.total_value).replace(",", ".")
        except Exception as e:
            print(f"Error formatting total value: {e}")
            return str(obj.total_value)