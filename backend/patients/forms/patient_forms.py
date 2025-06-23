from django import forms
from patients.models.core import Patient, Address, Contact, EmergencyContact

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'medical_record_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'address',
            'contact',
            'emergency_contact',
            # removed 'insurance' here since there's no Insurance model in core.py
        ]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['line1', 'line2', 'city', 'state', 'postal_code', 'country']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['phone', 'email']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone']
