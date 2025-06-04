# patients/views/api_rest.py

from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend

# pagination
from patients.api.pagination import PatientPagination

# models
from patients.models.core import Patient
from patients.models.billing import MedicationRequest
from patients.models.clinical import Condition, Allergy, Immunization, ClinicalData
from patients.models.encounter import Encounter, Observation
from patients.models.scheduling import Provider, Availability, Appointment
from patients.models.reporting import Notification
from patients.models.audit_log import AuditLog

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
    AuditLogSerializer,
    UserProfileSerializer,
    InventoryItemSerializer,
)


class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Read‐only for everyone; write/update/delete only if user is in “Doctor” group.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='Doctor').exists()
        )


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('contact', 'address', 'emergency_contact').all()
    serializer_class = PatientSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'medical_record_number']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
    schema = None  # disable automatic schema generation if you have a mismatch
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
    List, create, retrieve, and mark notifications as read.
    Each user sees only their own notifications.
    """
    queryset = Notification.objects.select_related('recipient', 'appointment').all()
    serializer_class = NotificationSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)


# ── New: Current User Profile Endpoint ─────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Returns: { "username": ..., "first_name": ..., "last_name": ..., "groups": [...] }
    Used by Dashboard to fetch profile data.
    """
    user = request.user
    group_names = [g.name for g in user.groups.all()]
    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'groups': group_names
    }
    return Response(data, status=status.HTTP_200_OK)


# ── New: AuditLog ViewSet ────────────────────────────────────────────────────────

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows admins (and authenticated users if you wish) to list/retrieve audit log entries,
    ordered by timestamp descending.
    """
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    pagination_class = PatientPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']  # default newest first
    permission_classes = [permissions.IsAdminUser]


# ── New: Low‐Stock Inventory Endpoint (Stub) ─────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def low_stock_inventory(request):
    """
    Returns the first five items where stock_level <= threshold.
    If you have a real InventoryItem model, substitute below.
    """
    # Example stub:
    # items = InventoryItem.objects.filter(stock_level__lte=F('threshold'))[:5]
    # serializer = InventoryItemSerializer(items, many=True)
    # return Response({'results': serializer.data})

    # If you don’t yet have an InventoryItem model, just return empty or fake:
    return Response({'results': []}, status=status.HTTP_200_OK)
