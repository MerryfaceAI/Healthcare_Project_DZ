# patients/urls/html.py

from django.urls import path
from patients.views.base import (
    PatientListView, PatientCreateView, PatientDetailView,
    PatientUpdateView, PatientDeleteView
)
from patients.views.medication import (
    MedicationRequestListView, MedicationRequestCreateView
)
from patients.views.pdf_export import PatientPDFView
from patients.views.api import PatientCSVView
from patients.views.reports import AppointmentsByWeekView, TopConditionsView

app_name = 'html'

urlpatterns = [
    # Core patients CRUD
    path('',               PatientListView.as_view(),   name='patient_list'),
    path('add/',           PatientCreateView.as_view(), name='add_patient'),
    path('<int:pk>/',      PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='edit_patient'),
    path('<int:pk>/delete/',PatientDeleteView.as_view(), name='delete_patient'),
    path('<int:pk>/pdf/',  PatientPDFView.as_view(),    name='patient_pdf'),

    # Exports & reports
    path('export/csv/',                        PatientCSVView.as_view(),           name='export_csv'),
    path('reports/appointments-by-week/',      AppointmentsByWeekView.as_view(),   name='reports_appointments_by_week'),
    path('reports/top-conditions/',            TopConditionsView.as_view(),        name='reports_top_conditions'),

    # Medication
    path('medications/',        MedicationRequestListView.as_view(),   name='medication_list'),
    path('medications/add/',    MedicationRequestCreateView.as_view(), name='add_medication'),
]
