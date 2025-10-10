from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bookings.models import Room, Reservation, Notification, UserProfile, Reminder
import traceback
import sys


def debug_admin_rooms(request):
    """Debug endpoint to check admin room management functionality"""
    try:
        debug_info = {
            'status': 'success',
            'debug_info': {
                'python_version': sys.version,
                'django_version': '4.2.7',
                'database_status': 'Connected',
                'admin_exists': False,
                'admin_has_profile': False,
                'room_count': 0,
                'rooms_sample': [],
                'forms_import_status': 'Checking...',
                'views_import_status': 'Checking...',
                'urls_import_status': 'Checking...',
                'templates_status': 'Checking...',
                'error_details': None
            }
        }
        
        # Check admin user
        try:
            admin_user = User.objects.get(username='admin')
            debug_info['debug_info']['admin_exists'] = True
            debug_info['debug_info']['admin_has_profile'] = hasattr(admin_user, 'profile')
        except User.DoesNotExist:
            debug_info['debug_info']['admin_exists'] = False
        
        # Check rooms
        try:
            rooms = Room.objects.all()[:5]
            debug_info['debug_info']['room_count'] = Room.objects.count()
            debug_info['debug_info']['rooms_sample'] = [
                {
                    'id': room.id,
                    'name': room.name,
                    'capacity': room.capacity,
                    'is_active': room.is_active
                } for room in rooms
            ]
        except Exception as e:
            debug_info['debug_info']['room_error'] = str(e)
        
        # Check forms import
        try:
            from bookings.forms import RoomForm
            debug_info['debug_info']['forms_import_status'] = 'Success'
        except Exception as e:
            debug_info['debug_info']['forms_import_status'] = f'Error: {str(e)}'
            debug_info['debug_info']['error_details'] = traceback.format_exc()
        
        # Check views import
        try:
            from bookings.views import admin_room_add, admin_room_edit, admin_room_delete
            debug_info['debug_info']['views_import_status'] = 'Success'
        except Exception as e:
            debug_info['debug_info']['views_import_status'] = f'Error: {str(e)}'
            debug_info['debug_info']['error_details'] = traceback.format_exc()
        
        # Check URLs
        try:
            from django.urls import reverse
            reverse('admin_room_add')
            reverse('admin_room_edit', args=[1])
            reverse('admin_room_delete', args=[1])
            debug_info['debug_info']['urls_import_status'] = 'Success'
        except Exception as e:
            debug_info['debug_info']['urls_import_status'] = f'Error: {str(e)}'
            debug_info['debug_info']['error_details'] = traceback.format_exc()
        
        return JsonResponse(debug_info)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        })
