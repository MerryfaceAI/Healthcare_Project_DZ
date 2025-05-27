# patients/views/medication.py

from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from patients.models.billing import MedicationRequest
from patients.forms.medication_form import MedicationRequestForm

class MedicationRequestListView(ListView):
    model = MedicationRequest
    template_name = 'patients/medications/medication_list.html'
    context_object_name = 'medications'

class MedicationRequestCreateView(CreateView):
    model = MedicationRequest
    form_class = MedicationRequestForm
    template_name = 'patients/medications/add_medication.html'
    success_url = reverse_lazy('patients:medication_list')
