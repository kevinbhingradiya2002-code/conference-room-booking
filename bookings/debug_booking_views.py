from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from bookings.models import Room, Reservation, UserProfile
from bookings.forms import ReservationForm
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def debug_booking(request):
    """Debug endpoint to test booking functionality"""
    try:
        # Get first available room
        room = Room.objects.filter(is_active=True).first()
        if not room:
            return JsonResponse({
                'status': 'error',
                'message': 'No rooms available'
            })
        
        # Test form creation
        form = ReservationForm(user=request.user, room_id=room.id)
        
        # Test room availability
        now = timezone.now()
        future_time = now + timedelta(hours=1)
        is_available = room.is_available(now, future_time)
        
        # Check user profile
        try:
            profile = request.user.profile
            has_profile = True
        except:
            has_profile = False
        
        # Test reservation creation (dry run)
        test_data = {
            'title': 'Test Booking',
            'description': 'Debug test',
            'start_time': now.strftime('%Y-%m-%dT%H:%M'),
            'end_time': future_time.strftime('%Y-%m-%dT%H:%M'),
            'room': room.id
        }
        
        test_form = ReservationForm(data=test_data, user=request.user, room_id=room.id)
        form_valid = test_form.is_valid()
        form_errors = test_form.errors if not form_valid else {}
        
        return JsonResponse({
            'status': 'success',
            'debug_info': {
                'user': request.user.username,
                'user_email': request.user.email,
                'has_profile': has_profile,
                'room_id': room.id,
                'room_name': room.name,
                'room_active': room.is_active,
                'room_available': is_available,
                'form_valid': form_valid,
                'form_errors': form_errors,
                'current_time': now.isoformat(),
                'test_start': test_data['start_time'],
                'test_end': test_data['end_time']
            }
        })
        
    except Exception as e:
        logger.error(f"Debug booking error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Debug failed: {str(e)}'
        })
