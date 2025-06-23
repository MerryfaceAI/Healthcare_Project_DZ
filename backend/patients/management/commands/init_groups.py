# patients/management/commands/init_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from patients.models.core import Patient
from patients.models import Appointment, Notification, ReportSnapshot

class Command(BaseCommand):
    help = 'Initialize roles and permissions for the healthcare system'

    def handle(self, *args, **options):
        # ─── Step 1: Create all groups ────────────────────────────
        admin_group, _       = Group.objects.get_or_create(name='Admin')
        doctor_group, _      = Group.objects.get_or_create(name='Doctor')
        nurse_group, _       = Group.objects.get_or_create(name='Nurse')
        reception_group, _   = Group.objects.get_or_create(name='Receptionist')
        billing_group, _     = Group.objects.get_or_create(name='Billing')

        # ─── Step 2: Define which models and perms we need ───────
        # For each model, we'll create the typical CRUD permissions:
        model_perms = {
            Patient:     ['view', 'add', 'change', 'delete'],
            Appointment: ['view', 'add', 'change', 'delete'],
            Notification:['view', 'add', 'change', 'delete'],
            ReportSnapshot:['view', 'add', 'change', 'delete'],
        }

        # ─── Step 3: Ensure each permission exists ───────────────
        for model, actions in model_perms.items():
            ct = ContentType.objects.get_for_model(model)
            for action in actions:
                codename = f'{action}_{model._meta.model_name}'
                name     = f'Can {action} {model._meta.verbose_name}'
                Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ct,
                    defaults={'name': name}
                )

        # ─── Step 4: Fetch Permission instances ──────────────────
        def perm(m, a): 
            return Permission.objects.get(
                codename=f'{a}_{m._meta.model_name}'
            )

        # Patient perms
        p_view   = perm(Patient, 'view')
        p_add    = perm(Patient, 'add')
        p_change = perm(Patient, 'change')
        p_delete = perm(Patient, 'delete')

        # Appointment perms
        a_view   = perm(Appointment, 'view')
        a_add    = perm(Appointment, 'add')
        a_change = perm(Appointment, 'change')
        a_delete = perm(Appointment, 'delete')

        # Notification perms
        n_view   = perm(Notification, 'view')
        n_add    = perm(Notification, 'add')
        n_change = perm(Notification, 'change')
        n_delete = perm(Notification, 'delete')

        # ReportSnapshot perms
        r_view   = perm(ReportSnapshot, 'view')
        r_add    = perm(ReportSnapshot, 'add')
        r_change = perm(ReportSnapshot, 'change')
        r_delete = perm(ReportSnapshot, 'delete')

        # ─── Step 5: Assign permissions to each group ────────────

        # Admin gets EVERYTHING
        all_perms = [
            p_view, p_add, p_change, p_delete,
            a_view, a_add, a_change, a_delete,
            n_view, n_add, n_change, n_delete,
            r_view, r_add, r_change, r_delete,
        ]
        admin_group.permissions.set(all_perms)

        # Doctor: can view & change patients, appointments, reports
        doctor_group.permissions.set([
            p_view, p_change,
            a_view, a_change,
            r_view,
        ])

        # Nurse: can view patients & appointments, add notifications
        nurse_group.permissions.set([
            p_view,
            a_view,
            n_view, n_add,
        ])

        # Receptionist: schedule patients (add/view appointments), view patients
        reception_group.permissions.set([
            p_view,
            a_view, a_add,
        ])

        # Billing: view patients, view appointments, add/view reports
        billing_group.permissions.set([
            p_view,
            a_view,
            r_view, r_add,
        ])

        self.stdout.write(self.style.SUCCESS('✅ Roles and permissions initialized.'))
