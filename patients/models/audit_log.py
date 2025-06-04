# patients/models/audit_log.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class AuditLog(models.Model):
    """
    Records every create/update/delete action on any model,
    who did it, when, on which object, and (optionally) what changed.
    """
    ACTION_CREATE = 'CREATE'
    ACTION_UPDATE = 'UPDATE'
    ACTION_DELETE = 'DELETE'
    ACTION_CHOICES = [
        (ACTION_CREATE, 'Create'),
        (ACTION_UPDATE, 'Update'),
        (ACTION_DELETE, 'Delete'),
    ]

    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text="When the action occurred"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Who performed the action"
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        help_text="Type of action"
    )

    # Generic relation to any model instance
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Type of the object changed"
    )
    object_id = models.CharField(
        max_length=255,
        help_text="Primary key of the object changed"
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Optional JSON snapshot of what changed
    changes = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON of the before/after state"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log Entries"

    def __str__(self):
        who = self.user.get_username() if self.user else "Anonymous"
        model_name = self.content_type.model_class().__name__
        return (
            f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] "
            f"{who} {self.action} {model_name}({self.object_id})"
        )
