from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from patients.models.core import Patient  # ✅ corrected import

class Command(BaseCommand):
    help = 'Initialize roles and permissions for the healthcare system'

    def handle(self, *args, **options):
        # Create Groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        nurse_group, _ = Group.objects.get_or_create(name='Nurse')

        # Patient permissions
        content_type = ContentType.objects.get_for_model(Patient)

        permissions = {
            'view_patient': 'Can view patient',
            'change_patient': 'Can change patient',
        }

        for codename, name in permissions.items():
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )

        # Assign permissions
        view_perm = Permission.objects.get(codename='view_patient')
        change_perm = Permission.objects.get(codename='change_patient')

        admin_group.permissions.set([view_perm, change_perm])
        doctor_group.permissions.set([view_perm])
        nurse_group.permissions.set([view_perm])

        self.stdout.write(self.style.SUCCESS('✅ Roles and permissions initialized.'))
