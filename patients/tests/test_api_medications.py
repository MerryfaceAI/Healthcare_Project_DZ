# patients/tests/test_api_medications.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from patients.models.core import Patient
from patients.models.billing import MedicationRequest


class MedicationRequestAPITest(APITestCase):
    def setUp(self):
        # — Create a Doctor user and authenticate —
        User = get_user_model()
        self.user = User.objects.create_user('doc1', 'doc1@example.com', 'pass123')
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        self.user.groups.add(doctor_group)
        self.client.force_authenticate(user=self.user)

        # — Create a patient to attach to the medication request —
        self.patient = Patient.objects.create(
            medical_record_number="MRN999",
            first_name="Bob",
            last_name="Jones",
            date_of_birth="1980-05-05",
            gender="M"
        )

        # — Endpoint and payload —
        self.list_url = reverse('patients:medicationrequest-list')
        self.data = {
            "patient": self.patient.id,
            "medication_name": "Aspirin",
            "dosage": "100mg",
            "frequency": "Once daily",
            "start_date": "2025-01-01",
            "end_date": "2025-02-01",
            "prescribing_doctor": "Dr. Who",
            "notes": "Take after meals"
        }

    def test_create_medication_request(self):
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            MedicationRequest.objects.filter(medication_name="Aspirin").exists()
        )

    def test_list_medication_requests(self):
        # Remove the 'patient' key from a copy so we don’t pass it twice
        payload = self.data.copy()
        payload.pop('patient')
        MedicationRequest.objects.create(patient=self.patient, **payload)

        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_update_medication_request(self):
        payload = self.data.copy()
        payload.pop('patient')
        mr = MedicationRequest.objects.create(patient=self.patient, **payload)

        detail_url = reverse('patients:medicationrequest-detail', args=(mr.id,))
        patch_data = {"notes": "Take with water"}

        response = self.client.patch(detail_url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mr.refresh_from_db()
        self.assertEqual(mr.notes, "Take with water")
