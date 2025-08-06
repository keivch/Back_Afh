from rest_framework import serializers
from .models import WorkAdvance
from exhibit.Serializer import ExhibitSerializer

class WorkAdvanceSerializer(serializers.ModelSerializer):
    exhibits = ExhibitSerializer(many=True, read_only=True)
    class Meta:
        model = WorkAdvance
        fields = '__all__'