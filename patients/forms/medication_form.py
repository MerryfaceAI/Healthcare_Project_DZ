from django import forms
from patients.models.billing import MedicationRequest

class MedicationRequestForm(forms.ModelForm):
    class Meta:
        model = MedicationRequest
        fields = '__all__'