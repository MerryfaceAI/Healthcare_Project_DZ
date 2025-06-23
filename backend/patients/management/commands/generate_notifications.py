import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from patients.models.scheduling import Appointment
from patients.models.reporting import Notification

class Command(BaseCommand):
    help = "Generate Notification objects for appointments coming up tomorrow."

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        start = datetime.datetime.combine(tomorrow, datetime.time.min, tzinfo=timezone.utc)
        end   = datetime.datetime.combine(tomorrow, datetime.time.max, tzinfo=timezone.utc)

        appts = Appointment.objects.filter(appointment_date__range=(start, end))
        created = 0
        for appt in appts:
            notif, was_new = Notification.objects.get_or_create(
                recipient=appt.patient.user,
                appointment=appt,
                defaults={
                    'message': f"Reminder: appointment on {appt.appointment_date.strftime('%Y-%m-%d %H:%M')}"
                }
            )
            if was_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} new reminder(s)."))
