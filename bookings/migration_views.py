from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.db import connection
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def force_migrate(request):
    """Force apply migrations and check database status"""
    try:
        # Apply migrations
        call_command('migrate', verbosity=0)
        
        # Check if reminder table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'bookings_reminder'
                )
            """)
            reminder_table_exists = cursor.fetchone()[0]
        
        # Check model counts
        from bookings.models import Room, Reservation, UserProfile, Notification, Reminder
        from django.contrib.auth.models import User
        
        counts = {
            'rooms': Room.objects.count(),
            'reservations': Reservation.objects.count(),
            'users': User.objects.count(),
            'profiles': UserProfile.objects.count(),
            'notifications': Notification.objects.count(),
            'reminders': Reminder.objects.count() if reminder_table_exists else 0,
        }
        
        return JsonResponse({
            'status': 'success',
            'message': 'Migrations applied successfully',
            'reminder_table_exists': reminder_table_exists,
            'counts': counts
        })
        
    except Exception as e:
        logger.error(f"Migration error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Migration failed: {str(e)}'
        })
