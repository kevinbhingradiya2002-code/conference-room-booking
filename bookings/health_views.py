from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import connection
from bookings.models import Room, UserProfile
import json


@csrf_exempt
def health_check(request):
    """Comprehensive health check for deployment"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test models
        user_count = User.objects.count()
        room_count = Room.objects.count()
        
        # Check if admin user exists
        admin_exists = User.objects.filter(username='admin').exists()
        admin_has_profile = False
        if admin_exists:
            admin_user = User.objects.get(username='admin')
            admin_has_profile = hasattr(admin_user, 'profile')
        
        return JsonResponse({
            'status': 'success',
            'message': 'Health check passed',
            'data': {
                'database_connected': True,
                'user_count': user_count,
                'room_count': room_count,
                'admin_exists': admin_exists,
                'admin_has_profile': admin_has_profile,
                'database_engine': connection.vendor,
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Health check failed: {str(e)}',
            'data': {
                'database_connected': False,
                'error_type': type(e).__name__,
            }
        })


@csrf_exempt
def create_admin_endpoint(request):
    """Create admin user via HTTP endpoint"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        # Create admin user if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            UserProfile.objects.create(user=admin_user, is_admin=True)
            return JsonResponse({
                'status': 'success',
                'message': 'Admin user created successfully',
                'credentials': 'admin/admin123'
            })
        else:
            # Update existing admin
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            
            if not hasattr(admin_user, 'profile'):
                UserProfile.objects.create(user=admin_user, is_admin=True)
            else:
                admin_user.profile.is_admin = True
                admin_user.profile.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Admin user updated successfully',
                'credentials': 'admin/admin123'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to create admin: {str(e)}'
        }, status=500)
