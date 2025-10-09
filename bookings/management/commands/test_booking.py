from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Room, Reservation
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Test room booking functionality'

    def handle(self, *args, **options):
        self.stdout.write('Testing room booking functionality...')
        
        user = User.objects.filter(is_superuser=False).first()
        if not user:
            self.stdout.write('No regular user found. Please run populate_data first.')
            return
        
        room = Room.objects.first()
        if not room:
            self.stdout.write('No room found. Please run populate_data first.')
            return
        
        start_time = timezone.now() + timedelta(hours=8)
        end_time = start_time + timedelta(hours=1)
        
        try:
            reservation = Reservation.objects.create(
                title='Test Booking',
                user=user,
                room=room,
                start_time=start_time,
                end_time=end_time,
                description='Testing booking functionality',
                status='confirmed'
            )
            
            self.stdout.write(f'[SUCCESS] Booking created successfully!')
            self.stdout.write(f'   User: {reservation.user.username}')
            self.stdout.write(f'   Room: {reservation.room.name}')
            self.stdout.write(f'   Time: {reservation.start_time} - {reservation.end_time}')
            self.stdout.write(f'   Status: {reservation.status}')
            
        except Exception as e:
            self.stdout.write(f'[ERROR] Booking failed: {str(e)}')
        
        self.stdout.write('Booking test completed!')
