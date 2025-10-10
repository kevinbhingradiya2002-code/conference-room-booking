from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    return JsonResponse({
        'status': 'success',
        'deployment_info': {
            'python_version': sys.version,
            'django_version': '4.2.7',
            'database_status': db_status,
            'environment_variables': {
                'DATABASE_URL': 'Set' if database_url != 'Not set' else 'Not set',
                'SECRET_KEY': 'Set' if secret_key != 'Not set' else 'Not set',
                'DEBUG': debug,
                'ALLOWED_HOSTS': allowed_hosts,
            }
        }
    })
