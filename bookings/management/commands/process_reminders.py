from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import Reminder
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process pending reminders and send notifications'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Find reminders that are due
        pending_reminders = Reminder.objects.filter(
            reminder_time__lte=now,
            is_sent=False
        )
        
        sent_count = 0
        for reminder in pending_reminders:
            try:
                reminder.send_reminder()
                sent_count += 1
                self.stdout.write(f"Sent reminder: {reminder}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error sending reminder {reminder.id}: {e}")
                )
                logger.error(f"Error sending reminder {reminder.id}: {e}")
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {sent_count} reminders")
        )
