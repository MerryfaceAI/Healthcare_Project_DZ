# patients/management/commands/runapscheduler.py

import time, logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from patients.jobs import send_appointment_reminders, delete_old_executions

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Starts APScheduler with reminder and cleanup jobs."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # send reminders every day at 8 AM
        scheduler.add_job(
        send_appointment_reminders,
        'interval',
        minutes=1,
        id='send_appointment_reminders',
        replace_existing=True,
    )

        # cleanup old executions weekly on Sunday midnight
        scheduler.add_job(
            delete_old_executions,
            'cron',
            day_of_week='sun',
            hour=0,
            minute=0,
            id='delete_old_executions',
            replace_existing=True,
        )

        self.stdout.write("Scheduler started. Ctrl+C to exit.")
        scheduler.start()

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            logger.info("Scheduler shut down.")
