from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import UserProfile


class Command(BaseCommand):
    help = 'Create admin user for production'

    def handle(self, *args, **options):
        try:
            if User.objects.filter(username='admin').exists():
                self.stdout.write('Admin user already exists')
                admin = User.objects.get(username='admin')
                admin.set_password('admin123')
                admin.save()
                
                if not hasattr(admin, 'profile'):
                    UserProfile.objects.create(user=admin, is_admin=True)
                    self.stdout.write('Admin profile created')
                else:
                    admin.profile.is_admin = True
                    admin.profile.save()
                    self.stdout.write('Admin profile updated')
                
                self.stdout.write('Admin password updated to: admin123')
            else:
                admin = User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                UserProfile.objects.create(user=admin, is_admin=True)
                self.stdout.write('Admin user created: admin/admin123')
        except Exception as e:
            self.stdout.write(f'Error creating admin: {str(e)}')
