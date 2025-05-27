from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from patients.models.core import Patient
from patients.models.scheduling import Provider, Availability, Appointment

User = get_user_model()

class SchedulingAPITest(APITestCase):
    def setUp(self):
        # make a “Doctor” user and authenticate
        self.user = User.objects.create_user('doc3', 'doc3@x.com', 'pass123')
        grp, _ = Group.objects.get_or_create(name='Doctor')
        self.user.groups.add(grp)
        self.client.force_authenticate(user=self.user)

        # create a patient and a provider
        self.patient = Patient.objects.create(
            medical_record_number="SCH01",
            first_name="Sched",
            last_name="Test",
            date_of_birth="1990-01-01",
            gender="U"
        )
        self.provider = Provider.objects.create(
            name="Dr. Scheduler",
            specialty="General",
            email="drsched@example.com",
            phone="555-1010"
        )

    def test_provider_crud(self):
        url = reverse('patients:provider-list')
        # CREATE
        resp = self.client.post(url, {
            "name": "Dr. Who",
            "specialty": "Time Travel",
            "email": "who@tardis.com",
            "phone": "000-0000"
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        pid = resp.data['id']

        # LIST
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(p['id']==pid for p in resp.data['results']))

        # UPDATE
        detail = reverse('patients:provider-detail', args=[pid])
        resp = self.client.patch(detail, {"specialty": "Universal"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['specialty'], "Universal")

    def test_availability_crud(self):
        url = reverse('patients:availability-list')
        resp = self.client.post(url, {
            "provider": self.provider.id,
            "weekday": 2,
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_appointment_crud(self):
        url = reverse('patients:appointment-list')
        resp = self.client.post(url, {
            "patient": self.patient.id,
            "provider": self.provider.id,
            "appointment_date": "2025-06-01T10:30:00Z",
            "reason": "Checkup",
            "status": "scheduled"
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
