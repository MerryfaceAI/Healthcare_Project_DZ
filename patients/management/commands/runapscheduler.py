import time
import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from patients.jobs import send_appointment_reminders
from patients.jobs import delete_old_executions

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Starts the APScheduler with reminder and cleanup jobs."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Schedule the appointment reminder job every hour to catch upcoming 24h window
        scheduler.add_job(
            send_appointment_reminders,
            trigger='cron',
            hour='*',
            minute='0',
            id='send_appointment_reminders',
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

        # Schedule cleanup weekly on Sunday at midnight
        scheduler.add_job(
            delete_old_executions,
            trigger='cron',
            day_of_week='sun',
            hour='0',
            minute='0',
            id='delete_old_executions',
            replace_existing=True
        )

        logger.info("Starting scheduler…")
        scheduler.start()

        try:
            self.stdout.write(self.style.SUCCESS("Scheduler started. Press Ctrl+C to exit."))
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down scheduler…")
            scheduler.shutdown()
