from django.db import models
from .core import Patient

class Provider(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.specialty})" if self.specialty else self.name


class Availability(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.provider.name} on {self.get_weekday_display()} from {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show')
        ],
        default='scheduled'
    )

    def __str__(self):
        return f"{self.patient} with {self.provider} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
