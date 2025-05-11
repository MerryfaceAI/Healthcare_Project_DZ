from django.db import models
from patients.models.core import Patient
from patients.models.encounter import Encounter

class Insurance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    group_number = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider} - {self.patient.name}"

class Claim(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    diagnosis_code = models.CharField(max_length=20)  # ICD code
    procedure_code = models.CharField(max_length=20)  # CPT code
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('pending', 'Pending'),
    ])
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.id} - {self.status}"

class Payment(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateField()

    def __str__(self):
        return f"Payment for Claim #{self.claim.id}"
