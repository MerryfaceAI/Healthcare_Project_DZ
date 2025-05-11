from django.db import models
from .core import Patient
from django.utils.translation import gettext_lazy as _

class MentalHealthAssessment(models.Model):
    class AssessmentType(models.TextChoices):
        DEPRESSION = 'depression', _('Depression')
        ANXIETY = 'anxiety', _('Anxiety')
        STRESS = 'stress', _('Stress')
        OTHER = 'other', _('Other')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='mental_assessments')
    assessment_type = models.CharField(max_length=50, choices=AssessmentType.choices)
    score = models.IntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assessment_type} - {self.patient.name} ({self.date})"

class TherapySession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='therapy_sessions')
    therapist_name = models.CharField(max_length=100)
    session_date = models.DateTimeField()
    session_notes = models.TextField()
    follow_up_needed = models.BooleanField(default=False)

    def __str__(self):
        return f"Therapy with {self.therapist_name} - {self.session_date.strftime('%Y-%m-%d')}"

class MentalHealthDiagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='mental_diagnoses')
    diagnosis = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    diagnosed_on = models.DateField()

    def __str__(self):
        return f"{self.diagnosis} - {self.patient.name}"
