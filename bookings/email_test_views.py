from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def test_email(request):
    """Test email configuration"""
    try:
        # Check email backend
        email_backend = settings.EMAIL_BACKEND
        
        # Check if SMTP credentials are available
        has_smtp = bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)
        
        # Try to send a test email
        test_subject = "Test Email from Conference Room Booking"
        test_message = f"""
Hello {request.user.username},

This is a test email from your conference room booking system.

If you receive this email, the email configuration is working correctly!

Email Backend: {email_backend}
SMTP Configured: {has_smtp}

Best regards,
Conference Room Booking System
        """
        
        try:
            send_mail(
                test_subject,
                test_message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            email_sent = True
            email_status = "Email sent successfully"
        except Exception as e:
            email_sent = False
            email_status = f"Email failed: {str(e)}"
        
        return JsonResponse({
            'status': 'success',
            'email_info': {
                'backend': email_backend,
                'smtp_configured': has_smtp,
                'user_email': request.user.email,
                'email_sent': email_sent,
                'email_status': email_status,
                'host': settings.EMAIL_HOST,
                'port': settings.EMAIL_PORT,
                'use_tls': settings.EMAIL_USE_TLS,
                'from_email': settings.DEFAULT_FROM_EMAIL,
            }
        })
        
    except Exception as e:
        logger.error(f"Email test error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Email test failed: {str(e)}'
        })
