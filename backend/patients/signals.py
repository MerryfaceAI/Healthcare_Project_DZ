# patients/signals.py
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models.core import Patient
from .models.audit_log import AuditLog

@receiver(pre_save, sender=Patient)
def log_patient_save(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(Patient)
    user = getattr(instance, '_current_user', None)
    action = 'update' if instance.pk else 'create'
    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=ct,
        object_id=str(instance.pk or 'new'),
        timestamp=timezone.now(),
        changes=None  # or diff JSON
    )

@receiver(pre_delete, sender=Patient)
def log_patient_delete(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(Patient)
    user = getattr(instance, '_current_user', None)
    AuditLog.objects.create(
        user=user,
        action='delete',
        content_type=ct,
        object_id=str(instance.pk),
        timestamp=timezone.now(),
        changes=None
    )
