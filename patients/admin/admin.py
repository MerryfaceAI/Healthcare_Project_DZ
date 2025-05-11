from django.contrib import admin
from .models import (
    Patient, MedicalHistory, ClinicalData,
    Appointment, Prescription, Document, FollowUp
)

# --- Inline Models ---
class MedicalHistoryInline(admin.StackedInline):
    model = MedicalHistory
    extra = 0

class ClinicalDataInline(admin.StackedInline):
    model = ClinicalData
    extra = 0

class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0

class PrescriptionInline(admin.StackedInline):
    model = Prescription
    extra = 0

class DocumentInline(admin.StackedInline):
    model = Document
    extra = 0

class FollowUpInline(admin.StackedInline):
    model = FollowUp
    extra = 0

# --- Patient Admin with Inlines ---
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('age',)
    inlines = [
        MedicalHistoryInline,
        ClinicalDataInline,
        AppointmentInline,
        PrescriptionInline,
        DocumentInline,
        FollowUpInline,
    ]

# Optional: Keep separate admin registrations (not strictly needed if using inlines)
@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnoses', 'allergies')

@admin.register(ClinicalData)
class ClinicalDataAdmin(admin.ModelAdmin):
    list_display = ('patient', 'blood_pressure', 'heart_rate', 'weight', 'created_at')
    list_filter = ('created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor_name', 'appointment_date')
    list_filter = ('appointment_date',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'title', 'uploaded_at')
    list_filter = ('uploaded_at',)

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'follow_up_date')
    list_filter = ('follow_up_date',)
