from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Room, Reservation, Notification
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create test reservations and notifications'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        user = User.objects.first()
        if not user:
            self.stdout.write('No users found. Please run populate_data first.')
            return
        
        room = Room.objects.first()
        if not room:
            self.stdout.write('No rooms found. Please run populate_data first.')
            return
        
        start_time = timezone.now() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=1)
        
        reservation, created = Reservation.objects.get_or_create(
            title='Test Meeting',
            user=user,
            room=room,
            start_time=start_time,
            end_time=end_time,
            defaults={
                'description': 'This is a test reservation',
                'status': 'confirmed'
            }
        )
        
        if created:
            Notification.objects.create(
                user=user,
                reservation=reservation,
                notification_type='reservation_confirmed',
                message=f'Your reservation for {room.name} has been confirmed for {reservation.start_time.strftime("%Y-%m-%d %H:%M")}.'
            )
            
            Notification.objects.create(
                user=user,
                reservation=reservation,
                notification_type='reservation_reminder',
                message=f'Reminder: Your meeting "{reservation.title}" starts in 1 hour.'
            )
            
            self.stdout.write('Test data created successfully!')
            self.stdout.write(f'Created reservation: {reservation.title}')
            self.stdout.write(f'Created notifications for user: {user.username}')
        else:
            self.stdout.write('Test reservation already exists.')
        
        self.stdout.write('Test data creation completed!')
