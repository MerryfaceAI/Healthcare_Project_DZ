from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from patients.models.core import Patient
from weasyprint import HTML
import os
import csv


class PatientListView(PermissionRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    permission_required = 'patients.view_patient'

    def get_paginate_by(self, queryset):
        return int(self.request.GET.get('page_size', 10))

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('search_name')
        email = self.request.GET.get('search_email')
        age_group = self.request.GET.get('filter_age')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if age_group and age_group != 'all':
            if age_group == '0-18':
                queryset = queryset.filter(age__lte=18)
            elif age_group == '19-40':
                queryset = queryset.filter(age__gte=19, age__lte=40)
            elif age_group == '41-65':
                queryset = queryset.filter(age__gte=41, age__lte=65)
            elif age_group == '65+':
                queryset = queryset.filter(age__gte=66)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_name': self.request.GET.get('search_name', '').strip(),
            'search_email': self.request.GET.get('search_email', '').strip(),
            'filter_age': self.request.GET.get('filter_age', ''),
            'page_size': int(self.request.GET.get('page_size', 10)),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('patients/includes/patient_table.html', context, request=request)
            return JsonResponse({'html': html})

        return self.render_to_response(context)


class PatientDetailView(PermissionRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'
    permission_required = 'patients.view_patient'


class PatientCreateView(PermissionRequiredMixin, CreateView):
    model = Patient
    fields = ['name', 'email', 'age']
    template_name = 'patients/add_patient.html'
    success_url = reverse_lazy('patients:patient_list')
    permission_required = 'patients.add_patient'


class PatientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Patient
    fields = ['name', 'email', 'age']
    template_name = 'patients/edit_patient.html'
    success_url = reverse_lazy('patients:patient_list')
    permission_required = 'patients.change_patient'


class PatientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('patients:patient_list')
    template_name = 'patients/confirm_delete.html'
    permission_required = 'patients.delete_patient'


class PatientPDFView(View):
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        html_string = render_to_string('patients/pdf_template.html', {'patient': patient})

        tmp_path = os.path.join(settings.BASE_DIR, 'tmp')
        os.makedirs(tmp_path, exist_ok=True)

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf(stylesheets=[], presentational_hints=True)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="patient_{patient.id}.pdf"'
        return response


class PatientCSVView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="patients.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Age'])

        for patient in Patient.objects.all():
            writer.writerow([patient.name, patient.email, patient.age])

        return response
