# patients/models/encounter.py

from django.db import models
from .core import Patient

class Encounter(models.Model):
    ENCOUNTER_TYPES = [
        ('visit', 'Visit'),
        ('phone', 'Phone'),
        ('telehealth', 'Telehealth'),
        ('other', 'Other'),
    ]
    patient = models.ForeignKey(
        Patient,
        related_name='encounters',
        on_delete=models.CASCADE
    )
    encounter_type = models.CharField(max_length=100, choices=ENCOUNTER_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    procedures = models.TextField(blank=True)
    notes = models.TextField(blank=True)  # renamed from `reason`

    def __str__(self):
        end = self.end_time.strftime('%Y-%m-%d %H:%M') if self.end_time else "ongoing"
        return (
            f"{self.encounter_type} for {self.patient} "
            f"from {self.start_time:%Y-%m-%d %H:%M} to {end} – "
            f"{self.notes[:30]}…"
        )


class Observation(models.Model):
    encounter = models.ForeignKey(
        Encounter,
        related_name='observations',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=50)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    observed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.code}: {self.value}{self.unit} @ {self.observed_at}"
