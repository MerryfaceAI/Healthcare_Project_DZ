from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# HTML & export views
from patients.views.base import (
    PatientListView, PatientCreateView, PatientDetailView,
    PatientUpdateView, PatientDeleteView,
)
from patients.views.reports import AppointmentsByWeekView, TopConditionsView
from patients.views.pdf_export import PatientPDFView
from patients.views.api import PatientCSVView
from patients.views.medication import (
    MedicationRequestListView, MedicationRequestCreateView,
)

# DRF ViewSets (core, clinical, encounter, scheduling)
from patients.views.api_rest import (
     PatientViewSet,
     MedicationRequestViewSet,
     ConditionViewSet,
     AllergyViewSet,
     ImmunizationViewSet,
     ClinicalDataViewSet,
     EncounterViewSet,
     ObservationViewSet,
     ProviderViewSet,
     AvailabilityViewSet,
     AppointmentViewSet,
     NotificationViewSet,
)

app_name = 'patients'

# DRF router setup
router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'medications', MedicationRequestViewSet, basename='medicationrequest')
router.register(r'conditions', ConditionViewSet, basename='condition')
router.register(r'allergies', AllergyViewSet, basename='allergy')
router.register(r'immunizations', ImmunizationViewSet, basename='immunization')
router.register(r'clinical-data', ClinicalDataViewSet, basename='clinicaldata')
router.register(r'encounters', EncounterViewSet, basename='encounter')
router.register(r'observations', ObservationViewSet, basename='observation')

# Scheduling & notifications
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'availabilities', AvailabilityViewSet, basename='availability')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # DRF browsable & JSON API
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Core HTML views
    path('', PatientListView.as_view(), name='patient_list'),
    path('add/', PatientCreateView.as_view(), name='add_patient'),
    path('detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='edit_patient'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='delete_patient'),
    path('<int:pk>/pdf/', PatientPDFView.as_view(), name='patient_pdf'),

    # CSV export
    path('export/csv/', PatientCSVView.as_view(), name='export_csv'),

    # Medication HTML views
    path('medications/', MedicationRequestListView.as_view(), name='medication_list'),
    path('medications/add/', MedicationRequestCreateView.as_view(), name='add_medication'),

    # Reports
    path('api/reports/appointments-by-week/', AppointmentsByWeekView.as_view(), name='reports-appointments-by-week'),
    path('api/reports/top-conditions/', TopConditionsView.as_view(), name='reports-top-conditions'),
]
