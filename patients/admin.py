# patients/admin.py

from django.contrib import admin
from patients.models.core import Patient, Address, Contact, EmergencyContact
from patients.models.billing import MedicationRequest
from patients.models.reporting import Notification

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('medical_record_number', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'medical_record_number')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('line1', 'city', 'state', 'country')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'phone')

@admin.register(MedicationRequest)
class MedicationRequestAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'patient', 'start_date', 'end_date')
    search_fields = ('medication_name', 'patient__medical_record_number')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'appointment', 'message', 'is_read', 'created_at')
    list_filter  = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')

    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"