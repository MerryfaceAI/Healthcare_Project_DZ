from rest_framework import viewsets, filters, permissions

# pagination
from patients.api.pagination import PatientPagination

# models
from patients.models.core import Patient
from patients.models.billing import MedicationRequest
from patients.models.clinical import Condition, Allergy, Immunization, ClinicalData
from patients.models.encounter import Encounter, Observation
from patients.models.scheduling import Provider, Availability, Appointment
from patients.models.reporting import Notification

# serializers
from patients.serializers import (
    PatientSerializer,
    MedicationRequestSerializer,
    ConditionSerializer,
    AllergySerializer,
    ImmunizationSerializer,
    ClinicalDataSerializer,
    EncounterSerializer,
    ObservationSerializer,
    ProviderSerializer,
    AvailabilitySerializer,
    AppointmentSerializer,
    NotificationSerializer,
)


class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Read-only for everyone; write/update/delete only for users in 'Doctor' group.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name='Doctor').exists()


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('contact', 'address', 'emergency_contact').all()
    serializer_class = PatientSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'medical_record_number']
    permission_classes = [permissions.AllowAny]


class MedicationRequestViewSet(viewsets.ModelViewSet):
    queryset = MedicationRequest.objects.select_related('patient').all()
    serializer_class = MedicationRequestSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['medication_name', 'patient__medical_record_number']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.select_related('patient').all()
    serializer_class = ConditionSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.select_related('patient').all()
    serializer_class = AllergySerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['substance', 'reaction']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class ImmunizationViewSet(viewsets.ModelViewSet):
    queryset = Immunization.objects.select_related('patient').all()
    serializer_class = ImmunizationSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['vaccine', 'lot_number']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class ClinicalDataViewSet(viewsets.ModelViewSet):
    queryset = ClinicalData.objects.select_related('patient').all()
    serializer_class = ClinicalDataSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['lab_results']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class EncounterViewSet(viewsets.ModelViewSet):
    # Disable schema generation for this view to avoid the EncounterSerializer mismatch
    schema = None
    queryset = Encounter.objects.select_related('patient').all()
    serializer_class = EncounterSerializer
    pagination_class = PatientPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.select_related('encounter').all()
    serializer_class = ObservationSerializer
    pagination_class = PatientPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    pagination_class = PatientPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.select_related('provider').all()
    serializer_class = AvailabilitySerializer
    pagination_class = PatientPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'provider').all()
    serializer_class = AppointmentSerializer
    pagination_class = PatientPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsDoctorOrReadOnly]


class NotificationViewSet(viewsets.ModelViewSet):
    """
    List, create, retrieve and mark notifications as read.
    """
    queryset = Notification.objects.select_related('recipient', 'appointment').all()
    serializer_class = NotificationSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # each user sees only their own notifications
        return super().get_queryset().filter(recipient=self.request.user)
