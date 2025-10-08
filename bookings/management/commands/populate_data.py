from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Room, UserProfile
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create rooms
        rooms_data = [
            {
                'name': 'Boardroom A',
                'capacity': 12,
                'location': 'Level 1, Building A',
                'description': 'Executive boardroom with panoramic city views. Perfect for important meetings and presentations.',
                'amenities': 'Projector, Whiteboard, Video Conferencing, Coffee Machine, Air Conditioning'
            },
            {
                'name': 'Conference Room B',
                'capacity': 8,
                'location': 'Level 2, Building A',
                'description': 'Modern conference room with state-of-the-art technology.',
                'amenities': 'Smart TV, Whiteboard, Video Conferencing, Air Conditioning'
            },
            {
                'name': 'Meeting Room C',
                'capacity': 6,
                'location': 'Level 1, Building B',
                'description': 'Intimate meeting space for small team discussions.',
                'amenities': 'Whiteboard, Air Conditioning, Natural Light'
            },
            {
                'name': 'Training Room D',
                'capacity': 20,
                'location': 'Level 3, Building A',
                'description': 'Large training facility with presentation capabilities.',
                'amenities': 'Projector, Whiteboard, Flip Charts, Air Conditioning, Sound System'
            },
            {
                'name': 'Executive Suite E',
                'capacity': 4,
                'location': 'Level 4, Building A',
                'description': 'Premium executive meeting room with luxury amenities.',
                'amenities': 'Smart TV, Video Conferencing, Coffee Machine, Air Conditioning, Premium Seating'
            },
            {
                'name': 'Collaboration Space F',
                'capacity': 10,
                'location': 'Level 2, Building B',
                'description': 'Open collaboration area with flexible seating arrangements.',
                'amenities': 'Whiteboard, Mobile Furniture, Air Conditioning, Natural Light'
            },
            {
                'name': 'Presentation Hall G',
                'capacity': 50,
                'location': 'Level 1, Building C',
                'description': 'Large presentation hall for company-wide meetings and events.',
                'amenities': 'Projector, Sound System, Stage, Air Conditioning, Seating for 50'
            },
            {
                'name': 'Focus Room H',
                'capacity': 2,
                'location': 'Level 3, Building B',
                'description': 'Small focus room for one-on-one meetings and private calls.',
                'amenities': 'Phone, Air Conditioning, Soundproofing'
            },
            {
                'name': 'Innovation Lab I',
                'capacity': 15,
                'location': 'Level 2, Building C',
                'description': 'Creative space designed for brainstorming and innovation sessions.',
                'amenities': 'Whiteboard, Flip Charts, Mobile Furniture, Air Conditioning, Creative Tools'
            },
            {
                'name': 'Client Meeting Room J',
                'capacity': 8,
                'location': 'Level 1, Building A',
                'description': 'Professional meeting room for client presentations and discussions.',
                'amenities': 'Smart TV, Video Conferencing, Air Conditioning, Professional Seating'
            }
        ]
        
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                name=room_data['name'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'Created room: {room.name}')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@tewharerunanga.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            # Create admin profile
            UserProfile.objects.create(user=admin_user, is_admin=True, department='IT')
            self.stdout.write('Created admin user: admin/admin123')
        
        # Create regular users
        users_data = [
            {
                'username': 'john.doe',
                'email': 'john.doe@tewharerunanga.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'department': 'Marketing'
            },
            {
                'username': 'jane.smith',
                'email': 'jane.smith@tewharerunanga.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'department': 'Sales'
            },
            {
                'username': 'mike.wilson',
                'email': 'mike.wilson@tewharerunanga.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'department': 'HR'
            },
            {
                'username': 'sarah.jones',
                'email': 'sarah.jones@tewharerunanga.com',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'department': 'Finance'
            },
            {
                'username': 'david.brown',
                'email': 'david.brown@tewharerunanga.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'department': 'Operations'
            }
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    department=user_data['department'],
                    phone_number=f'+64-{random.randint(20, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
                )
                self.stdout.write(f'Created user: {user.username}/password123')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('You can now login with:')
        self.stdout.write('- Admin: admin/admin123')
        self.stdout.write('- Users: john.doe/password123, jane.smith/password123, etc.')
