from django.urls import path
from .views import (
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    EditMedicalHistoryView,
    EditClinicalDataView,
    EditAppointmentsView,
    EditPrescriptionsView,
    EditDocumentsView,
    EditFollowUpView,
    PatientPDFView,
    PatientCSVView,
)

app_name = 'patients'

urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('add/', PatientCreateView.as_view(), name='add_patient'),

    # 👇 Now using "detail/<int:pk>/" instead of just "<int:pk>/"
    path('detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),

    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='edit_patient'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='delete_patient'),

    path('<int:pk>/edit_medical_history/', EditMedicalHistoryView.as_view(), name='edit_medical_history'),
    path('<int:pk>/edit_clinical_data/', EditClinicalDataView.as_view(), name='edit_clinical_data'),
    path('<int:pk>/edit_appointments/', EditAppointmentsView.as_view(), name='edit_appointments'),
    path('<int:pk>/edit_prescriptions/', EditPrescriptionsView.as_view(), name='edit_prescriptions'),
    path('<int:pk>/edit_documents/', EditDocumentsView.as_view(), name='edit_documents'),
    path('<int:pk>/edit_follow_up/', EditFollowUpView.as_view(), name='edit_follow_up'),
    path('<int:pk>/pdf/', PatientPDFView.as_view(), name='patient_pdf'),
    path('export/csv/', PatientCSVView.as_view(), name='export_csv'),
]
