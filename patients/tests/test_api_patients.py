from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from patients.models.core import Patient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from patients.api.pagination import PatientPagination

class PatientAPITest(APITestCase):
    def setUp(self):
        # Create a user and add them to the Doctor group
        User = get_user_model()
        self.user = User.objects.create_user('alice', 'a@b.com', 'pass123')
        doctor_group = Group.objects.get(name='Doctor')
        self.user.groups.add(doctor_group)

        # Authenticate
        self.client.force_authenticate(user=self.user)
        self.url = reverse('patients:patient-list')  # router name
        self.patient_data = {
            "medical_record_number": "MRN123",
            "first_name": "Alice",
            "last_name": "Smith",
            "date_of_birth": "1990-01-01",
            "gender": "F",
        }

    def test_create_patient(self):
        response = self.client.post(self.url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(medical_record_number="MRN123").exists())

    def test_list_patients(self):
        Patient.objects.create(**self.patient_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
