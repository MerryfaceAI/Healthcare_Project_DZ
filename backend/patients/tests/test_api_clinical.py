# patients/tests/test_api_clinical.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from patients.models.core import Patient
from patients.models.clinical import Condition, Allergy, Immunization

User = get_user_model()

class ClinicalAPITest(APITestCase):
    def setUp(self):
        # Log in as a “Doctor”
        self.user = User.objects.create_user('doc2', 'doc2@x.com', 'pass123')
        grp, _ = Group.objects.get_or_create(name='Doctor')
        self.user.groups.add(grp)
        self.client.force_authenticate(user=self.user)

        # Create a patient to attach to
        self.patient = Patient.objects.create(
            medical_record_number="CLIN01",
            first_name="Test",
            last_name="Patient",
            date_of_birth="2000-01-01",
            gender="U"
        )

    def test_condition_crud(self):
        url = reverse('patients:condition-list')
        data = {
            'patient': self.patient.id,
            'name': 'A01',                   # was 'code'
            'description': 'Test condition',
            'onset_date': '2025-05-01',      # was 'date_recorded'
            'resolved_date': None            # was 'status'
        }
        # CREATE
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        cid = resp.data['id']

        # LIST
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(c['id'] == cid for c in resp.data['results']))

        # UPDATE
        detail = reverse('patients:condition-detail', args=[cid])
        resp = self.client.patch(detail, {'description': 'Updated'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['description'], 'Updated')

    def test_allergy_crud(self):
        url = reverse('patients:allergy-list')
        data = {
            'patient': self.patient.id,
            'substance': 'Peanuts',
            'reaction': 'Hives',
            'severity': 'severe',
            # recorded_date is auto-set, so we don’t send it
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_immunization_crud(self):
        url = reverse('patients:immunization-list')
        data = {
            'patient': self.patient.id,
            'vaccine': 'FluShot',            # was 'vaccine_name'
            'date_given': '2025-04-15',      # was 'date_administered'
            'lot_number': 'LOT123',
            'notes': ''                      # new field, required by serializer
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
