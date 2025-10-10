from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import connection
from bookings.models import UserProfile, Room
import os


class Command(BaseCommand):
    help = 'Test database connection and fix authentication issues'

    def handle(self, *args, **options):
        self.stdout.write('Testing database connection and authentication...')
        
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('[PASS] Database connection successful')
            
            # Test models
            user_count = User.objects.count()
            room_count = Room.objects.count()
            self.stdout.write(f'[INFO] Users: {user_count}, Rooms: {room_count}')
            
            # Check admin user
            if User.objects.filter(username='admin').exists():
                admin = User.objects.get(username='admin')
                self.stdout.write(f'[PASS] Admin user exists: {admin.username}')
                
                # Test authentication
                auth_user = authenticate(username='admin', password='admin123')
                if auth_user:
                    self.stdout.write('[PASS] Admin authentication works')
                else:
                    self.stdout.write('[FAIL] Admin authentication failed - resetting password')
                    admin.set_password('admin123')
                    admin.save()
                    self.stdout.write('[FIXED] Admin password reset to: admin123')
                
                # Check profile
                if hasattr(admin, 'profile'):
                    self.stdout.write(f'[PASS] Admin has profile: is_admin={admin.profile.is_admin}')
                else:
                    self.stdout.write('[FIXING] Creating admin profile...')
                    UserProfile.objects.create(user=admin, is_admin=True)
                    self.stdout.write('[FIXED] Admin profile created')
            else:
                self.stdout.write('[FIXING] Creating admin user...')
                admin = User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                UserProfile.objects.create(user=admin, is_admin=True)
                self.stdout.write('[FIXED] Admin user created: admin/admin123')
            
            # Ensure we have rooms
            if Room.objects.count() == 0:
                self.stdout.write('[FIXING] Creating sample rooms...')
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
                
                self.stdout.write(f'[FIXED] Created {len(rooms_data)} rooms')
            
            self.stdout.write('Database and authentication setup completed successfully!')
            self.stdout.write('Login credentials: admin/admin123')
            
        except Exception as e:
            self.stdout.write(f'[ERROR] Setup failed: {str(e)}')
            import traceback
            self.stdout.write(traceback.format_exc())
