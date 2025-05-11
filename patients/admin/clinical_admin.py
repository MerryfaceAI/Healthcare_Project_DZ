from django.contrib import admin
from patients.models import (
    Condition, Allergy, Immunization, MedicationStatement, FamilyHistory
)

admin.site.register(Condition)
admin.site.register(Allergy)
admin.site.register(Immunization)
admin.site.register(MedicationStatement)
admin.site.register(FamilyHistory)
