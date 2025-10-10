from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
from bookings.models import Room, Reservation, Notification
import os


class Command(BaseCommand):
    help = 'Setup production database with migrations and admin user'

    def handle(self, *args, **options):
        self.stdout.write('Setting up production database...')
        
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=0)
            
            self.stdout.write('Creating admin user...')
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write('Admin user created: admin/admin123')
            else:
                self.stdout.write('Admin user already exists')
            
            self.stdout.write('Creating sample rooms...')
            if Room.objects.count() == 0:
                rooms_data = [
                    {'name': 'Conference Room A', 'capacity': 10, 'description': 'Large conference room with projector'},
                    {'name': 'Conference Room B', 'capacity': 8, 'description': 'Medium conference room'},
                    {'name': 'Meeting Room 1', 'capacity': 6, 'description': 'Small meeting room'},
                    {'name': 'Meeting Room 2', 'capacity': 4, 'description': 'Intimate meeting space'},
                    {'name': 'Boardroom', 'capacity': 12, 'description': 'Executive boardroom'},
                    {'name': 'Training Room', 'capacity': 15, 'description': 'Training and workshop space'},
                    {'name': 'Focus Room', 'capacity': 2, 'description': 'Quiet focus space'},
                    {'name': 'Collaboration Space', 'capacity': 6, 'description': 'Open collaboration area'},
                    {'name': 'Video Conference Room', 'capacity': 8, 'description': 'Equipped for video calls'},
                    {'name': 'Presentation Hall', 'capacity': 20, 'description': 'Large presentation space'},
                ]
                
                for room_data in rooms_data:
                    Room.objects.create(**room_data)
                
                self.stdout.write(f'Created {len(rooms_data)} rooms')
            else:
                self.stdout.write(f'Rooms already exist ({Room.objects.count()} total)')
            
            self.stdout.write('Production setup completed successfully!')
            
        except Exception as e:
            self.stdout.write(f'Error during setup: {str(e)}')
            raise
