import pytz
from rest_framework import serializers
from .models import Ticket
from tool.Serializer import ToolSerializer
from users.Serializers import UserSerializer

class TicketSerializer(serializers.ModelSerializer):
    tools = ToolSerializer(many=True)
    receiver = UserSerializer()
    applicant = UserSerializer()
    entry_date_formatted = serializers.SerializerMethodField()
    departure_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_entry_date_formatted(self, obj):
        zona_colombia = pytz.timezone('America/Bogota')
        fecha = obj.entry_date.astimezone(zona_colombia)
        return fecha.strftime("%d/%m/%Y %H:%M:%S")

    def get_departure_date_formatted(self, obj):
        if obj.departure_date is None:
            return "None"
        zona_colombia = pytz.timezone('America/Bogota')
        fecha = obj.departure_date.astimezone(zona_colombia)
        return fecha.strftime("%d/%m/%Y %H:%M:%S")
