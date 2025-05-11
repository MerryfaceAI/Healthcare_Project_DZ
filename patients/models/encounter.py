from django.db import models
from .core import Patient


class Encounter(models.Model):
    ENCOUNTER_TYPES = [
        ('inpatient', 'Inpatient'),
        ('outpatient', 'Outpatient'),
        ('emergency', 'Emergency'),
        ('telehealth', 'Telehealth'),
    ]

    patient = models.ForeignKey(Patient, related_name='encounters', on_delete=models.CASCADE)
    encounter_type = models.CharField(max_length=20, choices=ENCOUNTER_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_encounter_type_display()} - {self.patient} @ {self.start_time.date()}"


class Observation(models.Model):
    encounter = models.ForeignKey(Encounter, related_name='observations', on_delete=models.CASCADE)
    code = models.CharField(max_length=100)  # LOINC or standard terminology
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)
    observed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.code}: {self.value}{self.unit}"


class Procedure(models.Model):
    encounter = models.ForeignKey(Encounter, related_name='procedures', on_delete=models.CASCADE)
    procedure_code = models.CharField(max_length=100)  # CPT or ICD-10-PCS
    description = models.TextField()
    performed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.procedure_code} for {self.encounter.patient}"
