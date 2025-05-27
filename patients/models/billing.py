# patients/models/billing.py
from django.db import models
from patients.models.core import Patient

class MedicationRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_requests')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    prescribing_doctor = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication_name} for {self.patient}"
