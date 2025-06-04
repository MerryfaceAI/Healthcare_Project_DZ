# patients/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import (
    UserAdmin as DefaultUserAdmin,
    GroupAdmin as DefaultGroupAdmin
)
from django.contrib.auth.models import Group

from patients.models.core import Patient, Address, Contact, EmergencyContact
from patients.models.billing import MedicationRequest
from patients.models.reporting import Notification
from patients.models.audit_log import AuditLog

User = get_user_model()

# Unregister built-in registrations if they exist
for model in (User, Group):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# 1️⃣ Custom UserAdmin that shows groups
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = DefaultUserAdmin.list_display + ("groups_list",)
    list_filter  = DefaultUserAdmin.list_filter  + ("groups",)

    def groups_list(self, obj):
        return ", ".join(group.name for group in obj.groups.all())
    groups_list.short_description = "Groups"

# 2️⃣ Re-register Group with the default GroupAdmin (so it can be customized later)
@admin.register(Group)
class CustomGroupAdmin(DefaultGroupAdmin):
    pass  # or override list_display/search_fields here if you like

# 3️⃣ Your existing ModelAdmins
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
