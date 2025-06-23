from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import csv

from patients.models.core import Patient


class PatientCSVView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="patients_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "MRN", "First Name", "Last Name", "DOB", "Gender",
            "Phone", "Email",
            "Address", "Emergency Contact", "Insurance Provider", "Policy #", "Valid Until"
        ])

        for patient in Patient.objects.select_related(
            'contact', 'address', 'emergency_contact', 'insurance'
        ).all():
            writer.writerow([
                patient.medical_record_number,
                patient.first_name,
                patient.last_name,
                patient.date_of_birth,
                patient.get_gender_display(),
                getattr(patient.contact, 'phone', ''),
                getattr(patient.contact, 'email', ''),
                f"{patient.address.line1}, {patient.address.city}" if patient.address else '',
                f"{patient.emergency_contact.name} ({patient.emergency_contact.relationship}) - {patient.emergency_contact.phone}"
                    if patient.emergency_contact else '',
                getattr(patient.insurance, 'provider', ''),
                getattr(patient.insurance, 'policy_number', ''),
                getattr(patient.insurance, 'valid_until', '')
            ])

        return response


def patient_json_api_view(request):
    """
    JSON API endpoint that returns paginated and filterable patient data.
    Supports:
    - ?search=name_or_mrn
    - ?page=1
    - ?page_size=10
    """
    search = request.GET.get('search', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    queryset = Patient.objects.select_related('contact').all()

    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(medical_record_number__icontains=search)
        )

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    results = []
    for p in page_obj:
        results.append({
            'id': p.id,
            'mrn': p.medical_record_number,
            'first_name': p.first_name,
            'last_name': p.last_name,
            'date_of_birth': p.date_of_birth.isoformat(),
            'gender': p.get_gender_display(),
            'phone': p.contact.phone if p.contact else None,
            'email': p.contact.email if p.contact else None
        })

    return JsonResponse({
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': results
    })
