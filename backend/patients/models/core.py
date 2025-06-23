# patients/models/core.py

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from healthcare.middleware import get_current_user
from patients.models.audit_log import AuditLog


class Address(models.Model):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.country}"


class Contact(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.phone


class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='patient_profile'
    )
    medical_record_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    contact = models.OneToOneField(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    emergency_contact = models.OneToOneField(
        EmergencyContact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.medical_record_number})"

    def save(self, *args, **kwargs):
        # Determine if this is a create versus update
        is_create = self.pk is None

        # First, save the Patient record
        super().save(*args, **kwargs)

        # Now log to AuditLog
        user = get_current_user()
        ct = ContentType.objects.get_for_model(Patient)

        AuditLog.objects.create(
            user=user,
            action='create' if is_create else 'update',
            content_type=ct,
            object_id=str(self.pk),
            timestamp=timezone.now(),
            changes=None  # you can plug in a diff here if you want
        )
