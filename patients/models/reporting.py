from django.db import models
from patients.models.core import Patient

class QualityMetric(models.Model):
    METRIC_TYPES = [
        ('bp_control', 'Blood Pressure Control'),
        ('diabetes_mgmt', 'Diabetes Management'),
        ('med_adherence', 'Medication Adherence'),
        ('annual_visit', 'Annual Visit Compliance'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='quality_metrics')
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metric_type} for {self.patient} at {self.recorded_at.date()}"

class ReportSnapshot(models.Model):
    title = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"Report: {self.title} ({self.generated_at.date()})"
