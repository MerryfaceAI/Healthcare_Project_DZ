from django.contrib import admin
from patients.models import QualityMetric, ComplianceReport, CustomAnalytics

admin.site.register(QualityMetric)
admin.site.register(ComplianceReport)
admin.site.register(CustomAnalytics)
