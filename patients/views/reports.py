# patients/views/reports.py

from django.db.models import Count
from django.db.models.functions import TruncWeek
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

# FIXED imports:
from patients.models.scheduling import Appointment
from patients.models.clinical import Condition


class AppointmentsByWeekView(APIView):
    """
    GET /patients/api/reports/appointments-by-week/
    Returns a list of weeks (Mon-Sun) with the number of appointments in each.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = (
            Appointment.objects
            .annotate(week=TruncWeek('appointment_date'))
            .values('week')
            .annotate(count=Count('id'))
            .order_by('week')
        )
        data = [
            {'week': entry['week'].date().isoformat(), 'count': entry['count']}
            for entry in qs
        ]
        return Response(data)


class TopConditionsView(APIView):
    """
    GET /patients/api/reports/top-conditions/
    Returns the 10 most frequent condition names and their counts.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = (
            Condition.objects
            .values('name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        return Response(list(qs))
