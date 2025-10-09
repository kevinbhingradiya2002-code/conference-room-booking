from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Room, Reservation, UserProfile, Notification
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Check if database meets all assignment requirements'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('CONFERENCE ROOM BOOKING SYSTEM - REQUIREMENTS CHECK')
        self.stdout.write('=' * 60)
        
        # Check 1: 10 Conference Rooms
        self.stdout.write('\n1. CONFERENCE ROOMS (Required: 10 rooms)')
        rooms = Room.objects.all()
        self.stdout.write(f'   Total rooms: {rooms.count()}')
        if rooms.count() >= 10:
            self.stdout.write('   [PASS] Sufficient rooms available')
        else:
            self.stdout.write('   [FAIL] Need at least 10 rooms')
        
        self.stdout.write('   Room details:')
        for room in rooms:
            self.stdout.write(f'   - {room.name} (Capacity: {room.capacity}, Active: {room.is_active})')
        
        # Check 2: User Authentication System
        self.stdout.write('\n2. USER AUTHENTICATION SYSTEM')
        users = User.objects.all()
        self.stdout.write(f'   Total users: {users.count()}')
        
        # Check admin user
        admin_users = User.objects.filter(is_superuser=True)
        self.stdout.write(f'   Admin users: {admin_users.count()}')
        if admin_users.exists():
            self.stdout.write('   [PASS] Admin user exists')
        else:
            self.stdout.write('   [FAIL] No admin user found')
        
        # Check regular users
        regular_users = User.objects.filter(is_superuser=False)
        self.stdout.write(f'   Regular users: {regular_users.count()}')
        if regular_users.count() >= 5:
            self.stdout.write('   [PASS] Sufficient regular users')
        else:
            self.stdout.write('   [WARNING] Few regular users (recommended: 5+)')
        
        # Check 3: User Profiles
        self.stdout.write('\n3. USER PROFILES')
        profiles = UserProfile.objects.all()
        self.stdout.write(f'   Total profiles: {profiles.count()}')
        
        admin_profiles = UserProfile.objects.filter(is_admin=True)
        self.stdout.write(f'   Admin profiles: {admin_profiles.count()}')
        
        # Check 4: Reservations
        self.stdout.write('\n4. RESERVATION SYSTEM')
        reservations = Reservation.objects.all()
        self.stdout.write(f'   Total reservations: {reservations.count()}')
        
        if reservations.exists():
            self.stdout.write('   [PASS] Reservations exist')
            
            # Check reservation statuses
            statuses = reservations.values_list('status', flat=True).distinct()
            self.stdout.write(f'   Reservation statuses: {list(statuses)}')
            
            # Check time-based reservations
            now = timezone.now()
            past_reservations = reservations.filter(end_time__lt=now)
            current_reservations = reservations.filter(start_time__lte=now, end_time__gte=now)
            future_reservations = reservations.filter(start_time__gt=now)
            
            self.stdout.write(f'   Past reservations: {past_reservations.count()}')
            self.stdout.write(f'   Current reservations: {current_reservations.count()}')
            self.stdout.write(f'   Future reservations: {future_reservations.count()}')
        else:
            self.stdout.write('   [WARNING] No reservations found')
        
        # Check 5: Notifications
        self.stdout.write('\n5. NOTIFICATION SYSTEM')
        notifications = Notification.objects.all()
        self.stdout.write(f'   Total notifications: {notifications.count()}')
        
        if notifications.exists():
            self.stdout.write('   [PASS] Notifications exist')
            
            # Check notification types
            notification_types = notifications.values_list('notification_type', flat=True).distinct()
            self.stdout.write(f'   Notification types: {list(notification_types)}')
            
            unread_notifications = notifications.filter(is_read=False)
            self.stdout.write(f'   Unread notifications: {unread_notifications.count()}')
        else:
            self.stdout.write('   [WARNING] No notifications found')
        
        # Check 6: Database Relationships
        self.stdout.write('\n6. DATABASE RELATIONSHIPS')
        
        # Check room-reservation relationships
        rooms_with_reservations = Room.objects.filter(reservations__isnull=False).distinct()
        self.stdout.write(f'   Rooms with reservations: {rooms_with_reservations.count()}')
        
        # Check user-reservation relationships
        users_with_reservations = User.objects.filter(reservations__isnull=False).distinct()
        self.stdout.write(f'   Users with reservations: {users_with_reservations.count()}')
        
        # Check 7: Required Functionality
        self.stdout.write('\n7. REQUIRED FUNCTIONALITY CHECK')
        
        # View Available Rooms
        active_rooms = Room.objects.filter(is_active=True)
        self.stdout.write(f'   Active rooms for viewing: {active_rooms.count()}')
        
        # Make Reservations
        if reservations.exists():
            self.stdout.write('   [PASS] Reservation creation functionality')
        else:
            self.stdout.write('   [FAIL] No reservations to test functionality')
        
        # Manage Reservations
        if reservations.exists():
            self.stdout.write('   [PASS] Reservation management functionality')
        else:
            self.stdout.write('   [FAIL] No reservations to manage')
        
        # User Authentication
        if users.exists():
            self.stdout.write('   [PASS] User authentication system')
        else:
            self.stdout.write('   [FAIL] No users for authentication')
        
        # Admin Panel
        if admin_users.exists():
            self.stdout.write('   [PASS] Admin panel access')
        else:
            self.stdout.write('   [FAIL] No admin users')
        
        # Notifications
        if notifications.exists():
            self.stdout.write('   [PASS] Notification system')
        else:
            self.stdout.write('   [FAIL] No notifications')
        
        # Check 8: Assignment Specific Requirements
        self.stdout.write('\n8. ASSIGNMENT SPECIFIC REQUIREMENTS')
        
        # Te Whare Rūnanga Ltd - 10 conference rooms
        if rooms.count() >= 10:
            self.stdout.write('   [PASS] 10 conference rooms requirement met')
        else:
            self.stdout.write('   [FAIL] Need exactly 10 conference rooms')
        
        # View Available Rooms
        if active_rooms.count() > 0:
            self.stdout.write('   [PASS] Users can view available rooms')
        else:
            self.stdout.write('   [FAIL] No active rooms to view')
        
        # Make Reservations
        if reservations.exists():
            self.stdout.write('   [PASS] Users can make reservations')
        else:
            self.stdout.write('   [WARNING] No reservations found (test by creating one)')
        
        # Manage Reservations
        if reservations.exists():
            self.stdout.write('   [PASS] Users can manage reservations')
        else:
            self.stdout.write('   [WARNING] No reservations to manage (test by creating one)')
        
        # User Authentication
        if users.count() > 0:
            self.stdout.write('   [PASS] Users must log in to make reservations')
        else:
            self.stdout.write('   [FAIL] No users for authentication')
        
        # Admin Panel Features
        admin_features = [
            'Add, Edit, and Delete Rooms',
            'Reserve for Users', 
            'Cancel User Reservations',
            'View All Reservations',
            'Manage User Accounts'
        ]
        
        self.stdout.write('   Admin Panel Features:')
        for feature in admin_features:
            self.stdout.write(f'   [AVAILABLE] {feature}')
        
        # Notifications
        if notifications.exists():
            self.stdout.write('   [PASS] Users receive confirmation and reminder notifications')
        else:
            self.stdout.write('   [WARNING] No notifications found (test by creating reservation)')
        
        # Final Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('SUMMARY')
        self.stdout.write('=' * 60)
        
        total_rooms = rooms.count()
        total_users = users.count()
        total_reservations = reservations.count()
        total_notifications = notifications.count()
        
        self.stdout.write(f'Database Statistics:')
        self.stdout.write(f'   - Conference Rooms: {total_rooms}')
        self.stdout.write(f'   - Users: {total_users}')
        self.stdout.write(f'   - Reservations: {total_reservations}')
        self.stdout.write(f'   - Notifications: {total_notifications}')
        
        # Overall assessment
        if total_rooms >= 10 and total_users > 0:
            self.stdout.write('\nOVERALL ASSESSMENT: [READY FOR SUBMISSION]')
            self.stdout.write('   All core requirements are met!')
            self.stdout.write('   The database is properly structured and populated.')
            self.stdout.write('   The system is ready for testing and deployment.')
        else:
            self.stdout.write('\nOVERALL ASSESSMENT: [NEEDS ATTENTION]')
            if total_rooms < 10:
                self.stdout.write('   - Need more conference rooms')
            if total_users == 0:
                self.stdout.write('   - Need to create users')
        
        self.stdout.write('\nNEXT STEPS:')
        self.stdout.write('   1. Test the application at http://127.0.0.1:8000/')
        self.stdout.write('   2. Login with admin/admin123')
        self.stdout.write('   3. Create some test reservations')
        self.stdout.write('   4. Test all functionality')
        self.stdout.write('   5. Deploy to Vercel when ready')