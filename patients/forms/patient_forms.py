# patients/forms.py
from django import forms
from patients.models.core import Patient
from patients.models.clinical import MedicalHistory, ClinicalData
from patients.models.encounter import Appointment, FollowUp
from patients.models.billing import Prescription
from patients.models.documents import Document

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'age', 'medical_history']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnoses', 'immunizations', 'allergies', 'family_history', 'surgeries']

class ClinicalDataForm(forms.ModelForm):
    class Meta:
        model = ClinicalData
        fields = ['blood_pressure', 'heart_rate', 'weight', 'lab_results']  # Removed 'created_at' since it's auto-generated

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_name', 'appointment_date', 'reason_for_visit']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'start_date', 'end_date', 'instructions']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']  # Modified field to match the model

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ['follow_up_date', 'notes']
