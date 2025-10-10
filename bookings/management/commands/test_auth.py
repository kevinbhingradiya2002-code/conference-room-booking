from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from bookings.models import UserProfile, Room


class Command(BaseCommand):
    help = 'Test authentication system'

    def handle(self, *args, **options):
        self.stdout.write('Testing authentication system...')
        
        try:
            # Test 1: Check if admin user exists and can authenticate
            if User.objects.filter(username='admin').exists():
                admin = User.objects.get(username='admin')
                self.stdout.write(f'[PASS] Admin user exists: {admin.username}')
                
                # Test authentication
                auth_user = authenticate(username='admin', password='admin123')
                if auth_user:
                    self.stdout.write('[PASS] Admin authentication works')
                else:
                    self.stdout.write('[FAIL] Admin authentication failed')
                
                # Test profile
                if hasattr(admin, 'profile'):
                    self.stdout.write(f'[PASS] Admin has profile: is_admin={admin.profile.is_admin}')
                else:
                    self.stdout.write('[FAIL] Admin missing profile')
            else:
                self.stdout.write('[FAIL] Admin user does not exist')
            
            # Test 2: Check database connectivity
            user_count = User.objects.count()
            room_count = Room.objects.count()
            self.stdout.write(f'[PASS] Database connected: {user_count} users, {room_count} rooms')
            
            # Test 3: Create a test user
            test_username = 'testuser'
            if not User.objects.filter(username=test_username).exists():
                test_user = User.objects.create_user(
                    username=test_username,
                    email='test@example.com',
                    password='testpass123'
                )
                UserProfile.objects.create(user=test_user)
                self.stdout.write('[PASS] Test user created')
                
                # Test authentication
                auth_test = authenticate(username=test_username, password='testpass123')
                if auth_test:
                    self.stdout.write('[PASS] Test user authentication works')
                else:
                    self.stdout.write('[FAIL] Test user authentication failed')
            else:
                self.stdout.write('[PASS] Test user already exists')
            
            self.stdout.write('Authentication system test completed!')
            
        except Exception as e:
            self.stdout.write(f'[ERROR] Authentication test failed: {str(e)}')
