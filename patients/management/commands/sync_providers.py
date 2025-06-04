# patients/management/commands/sync_providers.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from patients.models.scheduling import Provider

User = get_user_model()

class Command(BaseCommand):
    help = "Create a Provider entry for every user in the 'Doctor' group, if one doesn't exist."

    def handle(self, *args, **options):
        try:
            doctor_group = Group.objects.get(name="Doctor")
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR("No group named 'Doctor' found."))
            return

        count_created = 0
        for user in User.objects.filter(groups=doctor_group):
            provider_obj, created = Provider.objects.get_or_create(
                user=user,
                defaults={
                    "name": f"{user.first_name} {user.last_name}",
                    "specialty": "General",
                    "email": user.email or "",
                    "phone": "",
                },
            )
            if created:
                count_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Synced Providers. {count_created} new Provider(s) created.")
        )
