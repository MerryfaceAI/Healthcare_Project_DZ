# patients/models/scheduling.py

from django.db import models
from .core import Patient
from django.conf import settings

# (Optional) If you no longer want Provider at all, you can delete this whole class.
# If you want to keep it for other purposes, you can leave it, but Appointment no longer references it.
class Provider(models.Model):
    # Legacy/optional: you can remove this entire class if you do not need it.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If this provider is a system user, link them here",
    )
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.specialty})"


class Availability(models.Model):
    # If you keep Provider above, Availability can remain. Otherwise remove or adapt as needed.
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.IntegerField(
        choices=[(i, day) for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.provider.name} on {self.get_weekday_display()} from {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')

    # Instead of linking to Provider, link directly to the User model for doctors
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select a doctor (must be a user in the 'Doctor' group)",
        related_name='appointments_as_provider'
    )

    appointment_date = models.DateTimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ],
        default='scheduled'
    )

    def __str__(self):
        provider_str = self.provider.get_full_name() if self.provider else "No Provider"
        return f"{self.patient} with {provider_str} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
