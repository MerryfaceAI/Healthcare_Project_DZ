# patients/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin as DefaultGroupAdmin
from django.contrib.auth.models import Group
from django import forms

from patients.models.core import Patient, Address, Contact, EmergencyContact
from patients.models.billing import MedicationRequest
from patients.models.reporting import Notification
from patients.models.audit_log import AuditLog
from patients.models.scheduling import Appointment

# User model
User = get_user_model()

# 1️⃣ Unregister built-in User and Group (we will re-register with customizations)
for model in (User, Group):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# 2️⃣ Custom UserAdmin to show groups in list_display
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = DefaultUserAdmin.list_display + ("groups_list",)
    list_filter  = DefaultUserAdmin.list_filter  + ("groups",)

    def groups_list(self, obj):
        return ", ".join(group.name for group in obj.groups.all())
    groups_list.short_description = "Groups"

# 3️⃣ Re-register Group with the default GroupAdmin
@admin.register(Group)
class CustomGroupAdmin(DefaultGroupAdmin):
    pass  # You can override list_display or search_fields here if desired

# 4️⃣ Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display   = ("medical_record_number", "first_name", "last_name", "date_of_birth")
    search_fields  = ("first_name", "last_name", "medical_record_number")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("line1", "city", "state", "country")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("phone", "email")

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "relationship", "phone")

@admin.register(MedicationRequest)
class MedicationRequestAdmin(admin.ModelAdmin):
    list_display  = ("medication_name", "patient", "start_date", "end_date")
    search_fields = ("medication_name", "patient__medical_record_number")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display   = ("recipient", "appointment", "message", "is_read", "created_at")
    list_filter    = ("is_read", "created_at")
    search_fields  = ("recipient__username", "message")
    actions        = ["mark_as_read"]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display   = ("timestamp", "user", "content_type", "object_id", "action")
    list_filter    = ("content_type", "action", "user")
    search_fields  = ("object_id", "changes")
    date_hierarchy = "timestamp"

# 5️⃣ Custom form for Appointment so provider dropdown only shows Doctor-group users
class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter 'provider' choices to only users in the "Doctor" group
        from django.contrib.auth.models import Group
        doctor_group = Group.objects.filter(name='Doctor').first()
        if doctor_group:
            self.fields['provider'].queryset = doctor_group.user_set.all()
        else:
            # If no "Doctor" group exists, show none
            self.fields['provider'].queryset = User.objects.none()

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    list_display = ('id', 'patient', 'provider', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    # Search by patient name or provider username/full_name
    search_fields = ('patient__first_name', 'patient__last_name', 'provider__username', 'provider__first_name', 'provider__last_name')
