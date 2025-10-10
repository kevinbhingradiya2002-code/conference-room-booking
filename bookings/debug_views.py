from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import os
import sys


@csrf_exempt
def deployment_status(request):
    """Check deployment status and configuration"""
    try:
        # Check environment variables
        database_url = os.environ.get('DATABASE_URL', 'Not set')
        secret_key = os.environ.get('SECRET_KEY', 'Not set')
        debug = os.environ.get('DEBUG', 'Not set')
        allowed_hosts = os.environ.get('ALLOWED_HOSTS', 'Not set')
        
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "Connected"
            
        # Check if admin user exists
        from django.contrib.auth.models import User
        from bookings.models import UserProfile
        
        admin_exists = User.objects.filter(username='admin').exists()
        admin_has_profile = False
        if admin_exists:
            admin_user = User.objects.get(username='admin')
            admin_has_profile = hasattr(admin_user, 'profile')
            
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
    except Exception as e:
        db_status = f"Error: {str(e)}"
        admin_exists = False
        admin_has_profile = False
        user_count = 0
        profile_count = 0
    
    return JsonResponse({
        'status': 'success',
        'deployment_info': {
            'python_version': sys.version,
            'django_version': '4.2.7',
            'database_status': db_status,
            'admin_exists': admin_exists,
            'admin_has_profile': admin_has_profile,
            'user_count': user_count,
            'profile_count': profile_count,
            'environment_variables': {
                'DATABASE_URL': 'Set' if database_url != 'Not set' else 'Not set',
                'SECRET_KEY': 'Set' if secret_key != 'Not set' else 'Not set',
                'DEBUG': debug,
                'ALLOWED_HOSTS': allowed_hosts,
            }
        }
    })


@csrf_exempt
def fix_database(request):
    """Fix database by running migrations and creating admin user"""
    try:
        # Run migrations
        call_command('migrate', verbosity=0)
        
        # Create admin user
        from django.contrib.auth.models import User
        from bookings.models import UserProfile
        
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_message = 'Admin user created'
        else:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_message = 'Admin user updated'
        
        # Create UserProfile for admin
        user_profile, profile_created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'is_admin': True}
        )
        
        if profile_created:
            profile_message = 'Admin profile created'
        else:
            user_profile.is_admin = True
            user_profile.save()
            profile_message = 'Admin profile updated'
        
        return JsonResponse({
            'status': 'success',
            'message': 'Database fixed successfully',
            'details': {
                'migrations': 'Completed',
                'admin_user': admin_message,
                'admin_profile': profile_message
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Database fix failed: {str(e)}'
        })
