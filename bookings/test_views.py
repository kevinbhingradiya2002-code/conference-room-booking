from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from bookings.models import Room
import json


@csrf_exempt
def test_deployment(request):
    """Test endpoint to verify deployment status"""
    try:
        # Test database connection
        user_count = User.objects.count()
        room_count = Room.objects.count()
        
        # Check if admin user exists
        admin_exists = User.objects.filter(username='admin').exists()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Deployment test successful',
            'data': {
                'user_count': user_count,
                'room_count': room_count,
                'admin_exists': admin_exists,
                'database_connected': True
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Deployment test failed: {str(e)}',
            'data': {
                'database_connected': False
            }
        })
