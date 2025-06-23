from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os

from patients.models.core import Patient

class PatientPDFView(View):
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        html_string = render_to_string('patients/export/patient_pdf.html', {'patient': patient})

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="patient_{patient.pk}.pdf"'
        return response
