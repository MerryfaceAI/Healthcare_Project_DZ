# patients/views/api_reports.py

from django.db.models import Count
from django.db.models.functions import TruncWeek
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from patients.models.scheduling import Appointment
from patients.models.clinical import Condition

class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # read-only open, but write restricted (we’re only reading here)
        return True

class AppointmentsByWeekView(APIView):
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
            { 'week': item['week'].date().isoformat(), 'count': item['count'] }
            for item in qs
        ]
        return Response(data)


class TopConditionsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = (
            Condition.objects
            .values('name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        # returns e.g. [{ 'name': 'Hypertension', 'count': 12 }, …]
        return Response(list(qs))
