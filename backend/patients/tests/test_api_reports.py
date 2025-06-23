# patients/tests/test_api_reports.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from patients.models.core import Patient
from patients.models.scheduling import Appointment
from patients.models.clinical import Condition

User = get_user_model()

class ReportsAPITest(APITestCase):
    def setUp(self):
        # any authenticated user can view reports
        self.user = User.objects.create_user(
            username='reporter',
            email='rep@example.com',
            password='pass123'
        )
        self.client.force_authenticate(user=self.user)

        # create a patient
        self.patient = Patient.objects.create(
            medical_record_number="RPT001",
            first_name="Rep",
            last_name="Tester",
            date_of_birth="1990-06-15",
            gender="U"
        )

        # two appointments in the week of 2025-05-05, one in the week of 2025-05-12
        Appointment.objects.create(
            patient=self.patient,
            provider=None,
            appointment_date="2025-05-06T10:00:00Z",
            reason="Checkup",
            status="scheduled"
        )
        Appointment.objects.create(
            patient=self.patient,
            provider=None,
            appointment_date="2025-05-08T14:00:00Z",
            reason="Follow-up",
            status="scheduled"
        )
        Appointment.objects.create(
            patient=self.patient,
            provider=None,
            appointment_date="2025-05-13T09:00:00Z",
            reason="Consult",
            status="scheduled"
        )

        # three conditions: two “Flu”, one “Cold”
        Condition.objects.create(
            patient=self.patient,
            name="Flu",
            description="",
            onset_date="2025-04-01"
        )
        Condition.objects.create(
            patient=self.patient,
            name="Flu",
            description="",
            onset_date="2025-04-02"
        )
        Condition.objects.create(
            patient=self.patient,
            name="Cold",
            description="",
            onset_date="2025-04-03"
        )

    def test_appointments_by_week(self):
        url = reverse('patients:reports-appointments-by-week')
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.data
        # we should have two week-buckets
        self.assertEqual(len(data), 2)

        # map ISO-dates to counts (truncweek yields Monday)
        counts = { item['week'][:10]: item['count'] for item in data }
        self.assertEqual(counts.get('2025-05-05'), 2)
        self.assertEqual(counts.get('2025-05-12'), 1)

    def test_top_conditions(self):
        url = reverse('patients:reports-top-conditions')
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.data
        # “Flu” should be first with count=2, then “Cold” with count=1
        self.assertGreaterEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Flu")
        self.assertEqual(data[0]['count'], 2)
        self.assertEqual(data[1]['name'], "Cold")
        self.assertEqual(data[1]['count'], 1)
