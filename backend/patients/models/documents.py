from django.db import models
from patients.models.core import Patient

class MedicalDocument(models.Model):
    DOCUMENT_TYPES = [
        ('lab', 'Lab Report'),
        ('radiology', 'Radiology Report'),
        ('discharge', 'Discharge Summary'),
        ('referral', 'Referral Letter'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.document_type} - {self.title} ({self.patient})"
