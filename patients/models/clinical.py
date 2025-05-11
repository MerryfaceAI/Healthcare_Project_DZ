from django.db import models
from .core import Patient


class Condition(models.Model):
    patient = models.ForeignKey(Patient, related_name='conditions', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # ICD-10 or SNOMED preferred
    description = models.TextField(blank=True)
    onset_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.patient})"


class Allergy(models.Model):
    patient = models.ForeignKey(Patient, related_name='allergies', on_delete=models.CASCADE)
    substance = models.CharField(max_length=100)
    reaction = models.CharField(max_length=200, blank=True)
    severity = models.CharField(max_length=50, blank=True)
    recorded_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.substance} - {self.patient}"


class Immunization(models.Model):
    patient = models.ForeignKey(Patient, related_name='immunizations', on_delete=models.CASCADE)
    vaccine = models.CharField(max_length=100)
    date_given = models.DateField()
    lot_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vaccine} - {self.patient}"


class ClinicalData(models.Model):
    patient = models.ForeignKey(Patient, related_name='clinical_data', on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=20, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    lab_results = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clinical data for {self.patient} on {self.recorded_at.date()}"
