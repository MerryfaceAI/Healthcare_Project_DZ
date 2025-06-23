from rest_framework import serializers
from patients.models.core import Patient, Contact, Address, EmergencyContact
from patients.models.billing import MedicationRequest
from patients.models.clinical import Condition, Allergy, Immunization, ClinicalData
from patients.models.encounter import Encounter, Observation
from patients.models.scheduling import Provider, Availability, Appointment
from patients.models.reporting import Notification
from django.contrib.auth import get_user_model
from patients.models.audit_log import AuditLog

class MedicationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationRequest
        fields = [
            'id', 'patient', 'medication_name', 'dosage', 'frequency',
            'start_date', 'end_date', 'prescribing_doctor', 'notes',
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['phone', 'email']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['line1', 'line2', 'city', 'state', 'postal_code', 'country']


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone']


class PatientSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(required=False)
    address = AddressSerializer(required=False)
    emergency_contact = EmergencyContactSerializer(required=False)

    class Meta:
        model = Patient
        fields = [
            'id', 'medical_record_number', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'created_at',
            'contact', 'address', 'emergency_contact',
        ]

    def create(self, validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)
        emergency_data = validated_data.pop('emergency_contact', None)
        patient = Patient.objects.create(**validated_data)
        if contact_data:
            Contact.objects.create(patient=patient, **contact_data)
        if address_data:
            Address.objects.create(patient=patient, **address_data)
        if emergency_data:
            EmergencyContact.objects.create(patient=patient, **emergency_data)
        return patient

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ('contact', 'address', 'emergency_contact'):
                continue
            setattr(instance, attr, value)
        instance.save()
        if 'contact' in validated_data:
            contact_obj, _ = Contact.objects.get_or_create(patient=instance)
            for k, v in validated_data['contact'].items(): setattr(contact_obj, k, v)
            contact_obj.save()
        if 'address' in validated_data:
            address_obj, _ = Address.objects.get_or_create(patient=instance)
            for k, v in validated_data['address'].items(): setattr(address_obj, k, v)
            address_obj.save()
        if 'emergency_contact' in validated_data:
            em_obj, _ = EmergencyContact.objects.get_or_create(patient=instance)
            for k, v in validated_data['emergency_contact'].items(): setattr(em_obj, k, v)
            em_obj.save()
        return instance


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'patient', 'name', 'description', 'onset_date', 'resolved_date']


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['id', 'patient', 'substance', 'reaction', 'severity', 'recorded_date']


class ImmunizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Immunization
        fields = ['id', 'patient', 'vaccine', 'date_given', 'lot_number', 'notes']


class ClinicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalData
        fields = [
            'id', 'patient', 'blood_pressure', 'heart_rate',
            'temperature', 'weight', 'lab_results', 'recorded_at',
        ]


class EncounterSerializer(serializers.ModelSerializer):
    procedures = serializers.JSONField()

    class Meta:
        model = Encounter
        fields = [
            'id', 'patient', 'encounter_type',
            'start_time', 'end_time', 'procedures', 'notes',
        ]


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['id', 'encounter', 'code', 'value', 'unit', 'observed_at']


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name', 'specialty', 'email', 'phone']


class AvailabilitySerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())

    class Meta:
        model = Availability
        fields = ['id', 'provider', 'weekday', 'start_time', 'end_time']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'provider', 'appointment_date', 'reason', 'status']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'appointment', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'recipient', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'groups']

    def get_groups(self, obj):
        return [g.name for g in obj.groups.all()]

class InventoryItemSerializer(serializers.Serializer):
    # Stub fields; replace with real ones if you have them
    id = serializers.IntegerField()
    name = serializers.CharField()
    stock_level = serializers.IntegerField()
    threshold = serializers.IntegerField()

class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    content_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'timestamp',
            'user',
            'action',
            'content_type',
            'object_id',
            'changes',
        ]
        read_only_fields = ['id', 'timestamp', 'user']