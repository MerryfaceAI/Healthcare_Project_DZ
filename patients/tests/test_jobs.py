from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from patients.jobs import send_appointment_reminders
from patients.models.scheduling import Appointment
from patients.models.reporting import Notification
from patients.models.core import Patient
from django.contrib.auth import get_user_model

User = get_user_model()

class ReminderJobTest(TestCase):
    def setUp(self):
        # doctor user & patient/user link
        self.user = User.objects.create_user('u','u@x','p')
        self.patient = Patient.objects.create(
            medical_record_number="JMPT01",
            first_name="Job",
            last_name="Tester",
            date_of_birth="1980-01-01",
            gender="U",
            user=self.user
        )
        # appointment 12 hours from now
        self.appt = Appointment.objects.create(
            patient=self.patient,
            provider=None,
            appointment_date=timezone.now() + timedelta(hours=12),
            reason="Test",
        )

    def test_reminder_created(self):
        # no notifications yet
        self.assertFalse(Notification.objects.exists())

        # run the job
        send_appointment_reminders()

        # now one notification
        notif = Notification.objects.get(appointment=self.appt)
        self.assertEqual(notif.recipient, self.user)
        self.assertIn("Reminder:", notif.message)
