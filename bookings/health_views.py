from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def health_check(request):
    """Simple health check endpoint to test if Django is working"""
    try:
        return JsonResponse({
            'status': 'ok',
            'message': 'Django server is running',
            'python_version': __import__('sys').version
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
