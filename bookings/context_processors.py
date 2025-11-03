from .models import Notification
from django.db import connection


def notification_count(request):
    try:
        if request.user.is_authenticated:
            # Check if database is ready
            connection.ensure_connection()
            unread_count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
            return {'unread_notifications_count': unread_count}
    except Exception:
        # If database is not ready or any error occurs, return 0
        pass
    return {'unread_notifications_count': 0}