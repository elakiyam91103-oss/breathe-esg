from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DataIngestion(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP Fuel/Procurement'),
        ('UTILITY', 'Utility Electricity'),
        ('TRAVEL', 'Corporate Travel'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    row_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.client} - {self.source_type} - {self.uploaded_at}"

class EmissionRecord(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
        ('REJECTED', 'Rejected'),
    ]
    SCOPE_CHOICES = [(1, 'Scope 1'), (2, 'Scope 2'), (3, 'Scope 3')]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ingestion = models.ForeignKey(DataIngestion, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=20)
    scope = models.IntegerField(choices=SCOPE_CHOICES)
    raw_category = models.CharField(max_length=255)
    raw_value = models.FloatField()
    raw_unit = models.CharField(max_length=50)
    period_start = models.DateField()
    period_end = models.DateField()
    normalized_kgco2e = models.FloatField()
    emission_factor = models.FloatField()
    emission_factor_source = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    flag_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_records'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} | {self.source_type} | {self.normalized_kgco2e} kgCO2e"

class AuditLog(models.Model):
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()
