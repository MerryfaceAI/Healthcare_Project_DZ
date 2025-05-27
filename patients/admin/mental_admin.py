from django.contrib import admin
from patients.models import MentalHealthAssessment, TherapySession, MentalHealthDiagnosis

admin.site.register(MentalHealthAssessment)
admin.site.register(TherapySession)
admin.site.register(MentalHealthDiagnosis)
