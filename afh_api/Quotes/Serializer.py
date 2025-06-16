from rest_framework import serializers
from .models import Quotes
from Customer.Serializer import CustomerSerializer
from Option.Serializer import OptionSerializer
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')



class QuotesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    options = OptionSerializer()

    iva_value = serializers.SerializerMethodField()
    utility_value = serializers.SerializerMethodField()
    unforeseen_value = serializers.SerializerMethodField()
    administration_value = serializers.SerializerMethodField()
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
            'administration_value'
        ]

    def get_iva_value(self, obj):
        try:
            return "${:,.0f}".format(obj.iva_value).replace(",", ".")
        except:
            return str(obj.iva_value)
    def get_utility_value(self, obj):
        try:
            return "${:,.0f}".format(obj.utility_value).replace(",", ".")
        except:
            return str(obj.utility_value)
    def get_unforeseen_value(self, obj):
        try:
            return "${:,.0f}".format(obj.unforeseen_value).replace(",", ".")
        except:
            return str(obj.unforeseen_value)
    def get_administration_value(self, obj):
        try:
            return "${:,.0f}".format(obj.administration_value).replace(",", ".")
        except:
            return str(obj.administration_value)