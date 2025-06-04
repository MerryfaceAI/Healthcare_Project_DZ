# patients/views/base.py
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from patients.models.core import Patient
from patients.forms.patient_forms import PatientForm  # adjust if your form module is named differently

class PatientListView(PermissionRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    permission_required = 'patients.view_patient'

    def get_paginate_by(self, queryset):
        return int(self.request.GET.get('page_size', 10))

    def get_queryset(self):
        queryset = super().get_queryset().select_related('contact')
        name = self.request.GET.get('search_name')
        mrn = self.request.GET.get('search_id')

        if name:
            queryset = (queryset.filter(first_name__icontains=name) |
                        queryset.filter(last_name__icontains=name))
        if mrn:
            queryset = queryset.filter(medical_record_number__icontains=mrn)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'request': self.request  # preserve filters in pagination links
        })
        return context


class PatientDetailView(PermissionRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'
    permission_required = 'patients.view_patient'


class PatientCreateView(PermissionRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/add_patient.html'
    success_url = reverse_lazy('patients:patient_list')
    permission_required = 'patients.add_patient'


class PatientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/edit_patient.html'
    success_url = reverse_lazy('patients:patient_list')
    permission_required = 'patients.change_patient'


class PatientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    context_object_name = 'patient'
    success_url = reverse_lazy('patients:patient_list')
    permission_required = 'patients.delete_patient'