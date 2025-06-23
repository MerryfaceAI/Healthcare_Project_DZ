from django.contrib import admin
from patients.models import Encounter, Observation, Procedure

admin.site.register(Encounter)
admin.site.register(Observation)
admin.site.register(Procedure)
