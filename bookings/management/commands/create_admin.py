from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin user for production'

    def handle(self, *args, **options):
        try:
            if User.objects.filter(username='admin').exists():
                self.stdout.write('Admin user already exists')
                admin = User.objects.get(username='admin')
                admin.set_password('admin123')
                admin.save()
                self.stdout.write('Admin password updated to: admin123')
            else:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write('Admin user created: admin/admin123')
        except Exception as e:
            self.stdout.write(f'Error creating admin: {str(e)}')
