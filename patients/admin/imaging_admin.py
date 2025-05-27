from django.contrib import admin
from patients.models import ImagingStudy

@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'study_type', 'study_date', 'radiologist')
    list_filter = ('study_type', 'study_date')
    search_fields = ('patient__name', 'radiologist')
