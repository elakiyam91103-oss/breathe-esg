from rest_framework import serializers
from .models import Client, DataIngestion, EmissionRecord, AuditLog

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class DataIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataIngestion
        fields = '__all__'

class EmissionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'