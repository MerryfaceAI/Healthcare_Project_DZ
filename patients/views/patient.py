from django.views import View
from django.shortcuts import render, redirect
from patients.forms import (
    PatientForm, AddressForm, ContactForm, EmergencyContactForm, InsuranceForm
)

class PatientCreateView(View):
    template_name = 'patients/add_patient.html'

    def get(self, request):
        return render(request, self.template_name, {
            'patient_form': PatientForm(),
            'address_form': AddressForm(),
            'contact_form': ContactForm(),
            'emergency_form': EmergencyContactForm(),
            'insurance_form': InsuranceForm(),
        })

    def post(self, request):
        patient_form = PatientForm(request.POST)
        address_form = AddressForm(request.POST)
        contact_form = ContactForm(request.POST)
        emergency_form = EmergencyContactForm(request.POST)
        insurance_form = InsuranceForm(request.POST)

        if all([
            patient_form.is_valid(),
            address_form.is_valid(),
            contact_form.is_valid(),
            emergency_form.is_valid(),
            insurance_form.is_valid()
        ]):
            address = address_form.save()
            contact = contact_form.save()
            emergency = emergency_form.save()
            insurance = insurance_form.save()

            patient = patient_form.save(commit=False)
            patient.address = address
            patient.contact = contact
            patient.emergency_contact = emergency
            patient.insurance = insurance
            patient.save()

            return redirect('patients:patient_list')

        return render(request, self.template_name, {
            'patient_form': patient_form,
            'address_form': address_form,
            'contact_form': contact_form,
            'emergency_form': emergency_form,
            'insurance_form': insurance_form,
        })
