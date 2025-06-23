# patients/urls/api.py

from django.urls import path, include
from rest_framework import routers

# Import the module that actually lives at patients/views/api_rest.py
from patients.views import api_rest

router = routers.DefaultRouter()
router.register(r'patients', api_rest.PatientViewSet, basename='patient')
router.register(r'medications', api_rest.MedicationRequestViewSet, basename='medicationrequest')
router.register(r'conditions', api_rest.ConditionViewSet, basename='condition')
router.register(r'allergies', api_rest.AllergyViewSet, basename='allergy')
router.register(r'immunizations', api_rest.ImmunizationViewSet, basename='immunization')
router.register(r'clinical-data', api_rest.ClinicalDataViewSet, basename='clinicaldata')
router.register(r'encounters', api_rest.EncounterViewSet, basename='encounter')
router.register(r'observations', api_rest.ObservationViewSet, basename='observation')
router.register(r'providers', api_rest.ProviderViewSet, basename='provider')
router.register(r'availabilities', api_rest.AvailabilityViewSet, basename='availability')
router.register(r'appointments', api_rest.AppointmentViewSet, basename='appointment')
router.register(r'notifications', api_rest.NotificationViewSet, basename='notification')
router.register(r'audit-logs', api_rest.AuditLogViewSet, basename='auditlog')
# (We do NOT register low_stock_inventory with the router, since it’s a simple function‐based view)

urlpatterns = [
    # Include all of the above routers under /api/
    path('', include(router.urls)),

    # “Who am I?” endpoint
    path('users/me/', api_rest.current_user, name='current-user'),

    # Stubbed low‐stock inventory endpoint
    path('inventory/low-stock/', api_rest.low_stock_inventory, name='low-stock'),
]
