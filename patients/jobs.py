# patients/jobs.py

import logging
from datetime import timedelta
from django.utils import timezone

from patients.models.scheduling import Appointment
from patients.models.reporting import Notification

logger = logging.getLogger(__name__)

def send_appointment_reminders():
    """
    Look for all appointments within the next 24 hours and
    create a Notification for each patient user.
    """
    now = timezone.now()
    cutoff = now + timedelta(hours=24)

    # appointments in the next 24h
    upcoming = Appointment.objects.filter(
        appointment_date__gte=now,
        appointment_date__lt=cutoff,
        status='scheduled'
    )

    for appt in upcoming:
        user = getattr(appt.patient, 'user', None)
        if not user:
            # skip if patient not linked to a User
            logger.warning(f"Skipping Appt {appt.pk}: no linked user")
            continue
        # avoid duplicate notifications
        if Notification.objects.filter(appointment=appt, recipient=user).exists():
            logger.debug(f"Already notified for Appt {appt.pk}")
            continue

        Notification.objects.create(
            recipient=user,
            appointment=appt,
            message=f"Reminder: appointment on {appt.appointment_date:%Y-%m-%d %H:%M}",
        )
        logger.info(f"Queued reminder for Appt {appt.pk}")


def delete_old_executions(max_age_seconds=604_800):
    """
    Weekly cleanup of APScheduler job execution history.
    """
    from django_apscheduler.models import DjangoJobExecution

    DjangoJobExecution.objects.delete_old_job_executions(max_age_seconds)
    logger.info(f"Deleted APScheduler job executions older than {max_age_seconds} seconds")
