# patients/tests/test_api_notifications.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from patients.models.reporting import Notification
from patients.models.scheduling import Appointment
from patients.models.core import Patient

User = get_user_model()

class NotificationAPITest(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user('user1', 'u1@x.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'u2@x.com', 'pass')

        # Make user1 “Doctor” so they can create appointments
        from django.contrib.auth.models import Group
        grp, _ = Group.objects.get_or_create(name='Doctor')
        self.user1.groups.add(grp)

        # Create a patient & appointment
        self.patient = Patient.objects.create(
            medical_record_number="NOTIF01",
            first_name="Notif",
            last_name="Tester",
            date_of_birth="1990-01-01",
            gender="U"
        )
        self.app = Appointment.objects.create(
            patient=self.patient,
            provider=None,
            appointment_date="2025-06-01T09:00:00Z",
            reason="Checkup",
        )

        # Create notifications for each user
        Notification.objects.create(
            recipient=self.user1,
            appointment=self.app,
            message="Reminder for your appointment",
        )
        Notification.objects.create(
            recipient=self.user2,
            appointment=self.app,
            message="Other user reminder",
        )

    def test_list_only_own_notifications(self):
        self.client.force_authenticate(self.user1)
        url = reverse('patients:notification-list')
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Should only see one notification (user1’s)
        self.assertEqual(len(resp.data['results']), 1)
        self.assertEqual(resp.data['results'][0]['recipient'], self.user1.pk)

    def test_mark_as_read(self):
        self.client.force_authenticate(self.user1)
        # Grab user1’s notification
        notif = Notification.objects.filter(recipient=self.user1).first()
        url = reverse('patients:notification-detail', args=[notif.pk])
        # PATCH is_read=True
        resp = self.client.patch(url, {'is_read': True}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
