from django.contrib import admin
from patients.models import Insurance, Claim, Payment
from patients.models.billing import MedicationRequest

admin.site.register(Insurance)
admin.site.register(Claim)
admin.site.register(Payment)

@admin.register(MedicationRequest)
class MedicationRequestAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'patient', 'start_date', 'end_date', 'prescribing_doctor')