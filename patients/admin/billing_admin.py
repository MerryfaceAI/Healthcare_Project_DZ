from django.contrib import admin
from patients.models import Insurance, Claim, Payment

admin.site.register(Insurance)
admin.site.register(Claim)
admin.site.register(Payment)
