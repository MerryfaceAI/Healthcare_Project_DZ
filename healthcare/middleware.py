# healthcare/middleware.py

import threading
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from patients.models.audit_log import AuditLog

_thread_locals = threading.local()

def get_current_user():
    """Return the currently logged-in user for this thread (or None)."""
    return getattr(_thread_locals, 'user', None)

class CurrentUserAndAuditMiddleware:
    """
    1. Stashes request.user onto thread-local storage so signals and jobs can call get_current_user().
    2. After each response, writes an AuditLog entry for authenticated users on non-static paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration when Django starts

    def __call__(self, request):
        # Before view: store user
        _thread_locals.user = getattr(request, 'user', None)
        # Call the view
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        # After view: optionally log
        user = getattr(request, 'user', None)

        # Skip if not an authenticated user
        if not (user and user.is_authenticated):
            return response

        # Skip static/media to reduce noise
        path = request.path
        if path.startswith(('/static/', '/media/')):
            return response

        # Create an “access” audit entry
        AuditLog.objects.create(
            user=user,
            action='update',  # you can add 'access' to your ACTION_CHOICES
            content_type=ContentType.objects.get_for_model(AuditLog),
            object_id=path,
            timestamp=timezone.now(),
            changes={
                'method': request.method,
                'status_code': response.status_code,
            }
        )

        return response
