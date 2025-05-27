# patients/jobs.py

import logging
from datetime import datetime, timedelta
from django.utils import timezone

from patients.models.scheduling import Appointment
from patients.models.reporting import Notification

logger = logging.getLogger(__name__)

def send_appointment_reminders():
    """
    Look for all appointments within the next 24 hours and
    create a Notification for each patient.
    """
    now = timezone.now()
    cutoff = now + timedelta(hours=24)

    upcoming = Appointment.objects.filter(
        appointment_date__gte=now,
        appointment_date__lt=cutoff,
        status='scheduled'
    )

    for appt in upcoming:
        # avoid duplicate reminders
        already = Notification.objects.filter(
            appointment=appt,
            recipient=appt.patient.user  # assuming your Patient → User link
        ).exists()
        if not already:
            Notification.objects.create(
                recipient=appt.patient.user,
                appointment=appt,
                message=f"Reminder: you have an appointment on {appt.appointment_date:%Y-%m-%d %H:%M}",
            )
            logger.info(f"Queued reminder for Appointment {appt.pk}")

    logger.info(f"Checked {upcoming.count()} upcoming appointments")
