# patients/urls/api.py

from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from patients.views.api_rest import (
    PatientViewSet, MedicationRequestViewSet,
    ConditionViewSet, AllergyViewSet, ImmunizationViewSet,
    ClinicalDataViewSet, EncounterViewSet, ObservationViewSet,
    ProviderViewSet, AvailabilityViewSet,
    AppointmentViewSet, NotificationViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('patients', PatientViewSet)
router.register('medications', MedicationRequestViewSet)
router.register('conditions', ConditionViewSet)
router.register('allergies', AllergyViewSet)
router.register('immunizations', ImmunizationViewSet)
router.register('clinical-data', ClinicalDataViewSet)
router.register('encounters', EncounterViewSet)
router.register('observations', ObservationViewSet)
router.register('providers', ProviderViewSet)
router.register('availabilities', AvailabilityViewSet)
router.register('appointments', AppointmentViewSet)
router.register('notifications', NotificationViewSet)

urlpatterns = [
    # DRF router (all viewsets)
    path('', include((router.urls, 'router'), namespace='v1')),

    # Schema & docs for this API
    path('schema/', SpectacularAPIView.as_view(),            name='schema'),
    path('docs/',   SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/',  SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
