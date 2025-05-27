from django.db import models
from .core import Patient

class TherapySession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='therapy_sessions')
    session_date = models.DateTimeField()
    therapist_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session with {self.therapist_name} on {self.session_date.date()}"


class MentalHealthAssessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='mental_assessments')
    assessment_type = models.CharField(max_length=100)  # e.g. PHQ-9, GAD-7
    score = models.IntegerField()
    date = models.DateField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assessment_type} on {self.date} (Score: {self.score})"
