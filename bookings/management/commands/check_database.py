from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User
from bookings.models import Room, Reservation, UserProfile, Notification, Reminder


class Command(BaseCommand):
    help = 'Force apply migrations and check database status'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('DATABASE MIGRATION AND STATUS CHECK')
        self.stdout.write('=' * 60)
        
        try:
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✓ Database connection successful')
            
            # Apply migrations
            self.stdout.write('\nApplying migrations...')
            call_command('migrate', verbosity=0)
            self.stdout.write('✓ Migrations applied successfully')
            
            # Check if tables exist
            self.stdout.write('\nChecking table existence...')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'bookings_%'
                    ORDER BY table_name
                """)
                tables = cursor.fetchall()
                
                expected_tables = [
                    'bookings_room',
                    'bookings_reservation', 
                    'bookings_notification',
                    'bookings_userprofile',
                    'bookings_reminder'
                ]
                
                existing_tables = [table[0] for table in tables]
                self.stdout.write(f'Existing tables: {existing_tables}')
                
                for table in expected_tables:
                    if table in existing_tables:
                        self.stdout.write(f'✓ {table} exists')
                    else:
                        self.stdout.write(f'✗ {table} missing')
            
            # Check model counts
            self.stdout.write('\nChecking model counts...')
            try:
                room_count = Room.objects.count()
                self.stdout.write(f'✓ Rooms: {room_count}')
            except Exception as e:
                self.stdout.write(f'✗ Rooms error: {e}')
            
            try:
                reservation_count = Reservation.objects.count()
                self.stdout.write(f'✓ Reservations: {reservation_count}')
            except Exception as e:
                self.stdout.write(f'✗ Reservations error: {e}')
            
            try:
                user_count = User.objects.count()
                self.stdout.write(f'✓ Users: {user_count}')
            except Exception as e:
                self.stdout.write(f'✗ Users error: {e}')
            
            try:
                profile_count = UserProfile.objects.count()
                self.stdout.write(f'✓ UserProfiles: {profile_count}')
            except Exception as e:
                self.stdout.write(f'✗ UserProfiles error: {e}')
            
            try:
                notification_count = Notification.objects.count()
                self.stdout.write(f'✓ Notifications: {notification_count}')
            except Exception as e:
                self.stdout.write(f'✗ Notifications error: {e}')
            
            try:
                reminder_count = Reminder.objects.count()
                self.stdout.write(f'✓ Reminders: {reminder_count}')
            except Exception as e:
                self.stdout.write(f'✗ Reminders error: {e}')
            
            # Create admin user if needed
            self.stdout.write('\nChecking admin user...')
            try:
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
                    self.stdout.write('✓ Admin user created')
                else:
                    self.stdout.write('✓ Admin user exists')
                
                # Ensure admin has profile
                profile, created = UserProfile.objects.get_or_create(
                    user=admin_user,
                    defaults={'is_admin': True}
                )
                if created:
                    self.stdout.write('✓ Admin profile created')
                else:
                    self.stdout.write('✓ Admin profile exists')
                    
            except Exception as e:
                self.stdout.write(f'✗ Admin user error: {e}')
            
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('DATABASE CHECK COMPLETE')
            self.stdout.write('=' * 60)
            
        except Exception as e:
            self.stdout.write(f'✗ Database check failed: {e}')
            raise
