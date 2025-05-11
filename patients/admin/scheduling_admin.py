from django.contrib import admin
from patients.models import Provider, Appointment, Reminder

admin.site.register(Provider)
admin.site.register(Appointment)
admin.site.register(Reminder)
