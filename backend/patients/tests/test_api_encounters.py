from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from patients.models.core import Patient
from patients.models.encounter import Encounter, Observation

User = get_user_model()

class EncounterAPITest(APITestCase):
    def setUp(self):
        # create a “Doctor” user and authenticate
        self.user = User.objects.create_user('doc', 'doc@example.com', 'pass123')
        grp, _ = Group.objects.get_or_create(name='Doctor')
        self.user.groups.add(grp)
        self.client.force_authenticate(self.user)

        # and a patient to attach encounters to
        self.patient = Patient.objects.create(
            medical_record_number="ENC01",
            first_name="Test",
            last_name="Patient",
            date_of_birth="1990-01-01",
            gender="U"
        )

    def test_create_and_list_encounter(self):
        url = reverse('patients:encounter-list')
        payload = {
            'patient': self.patient.id,
            'start_time': '2025-05-10T09:00:00Z',
            'end_time':   '2025-05-10T10:00:00Z',
            'reason':     'Routine check',
            'notes':      'All good',
            'procedures': ''
        }
        # CREATE
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        enc_id = resp.data['id']

        # LIST
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [e['id'] for e in resp.data['results']]
        self.assertIn(enc_id, ids)


class ObservationAPITest(APITestCase):
    def setUp(self):
        # same doctor + patient
        self.user = User.objects.create_user('doc2', 'doc2@example.com', 'pass123')
        grp, _ = Group.objects.get_or_create(name='Doctor')
        self.user.groups.add(grp)
        self.client.force_authenticate(self.user)

        self.patient = Patient.objects.create(
            medical_record_number="OBS01",
            first_name="Obs",
            last_name="Tester",
            date_of_birth="1985-12-12",
            gender="U"
        )

        # create one Encounter to attach observations to
        self.encounter = Encounter.objects.create(
            patient=self.patient,
            start_time='2025-05-10T09:00:00Z',
            end_time='2025-05-10T10:00:00Z',
            reason='Checkup',
            notes='',
            procedures=''
        )

    def test_create_and_list_observation(self):
        url = reverse('patients:observation-list')
        payload = {
            'encounter':  self.encounter.id,
            'code':       'BP',
            'value':      '120/80',
            'unit':       'mmHg',
            'observed_at':'2025-05-10T09:30:00Z'
        }
        # CREATE
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        obs_id = resp.data['id']

        # LIST
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [o['id'] for o in resp.data['results']]
        self.assertIn(obs_id, ids)
