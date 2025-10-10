from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    amenities = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

    def is_available(self, start_time, end_time, exclude_reservation=None):
        reservations = self.reservations.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='confirmed'
        )
        if exclude_reservation:
            reservations = reservations.exclude(id=exclude_reservation.id)
        return not reservations.exists()


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.room.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        
        if self.start_time < timezone.now():
            raise ValidationError("Cannot create reservation in the past.")
        
        if hasattr(self, 'room') and self.room:
            if not self.room.is_available(self.start_time, self.end_time, self):
                raise ValidationError("Room is not available for the selected time period.")
        
        if hasattr(self, 'user') and self.user:
            conflicting = Reservation.objects.filter(
                user=self.user,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
                status='confirmed'
            ).exclude(id=self.id)
            if conflicting.exists():
                raise ValidationError("You already have a reservation during this time period.")

    def save(self, *args, **kwargs):
        self.clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.status == 'confirmed':
            self.create_reminders()
            self.send_confirmation_email()

    def create_reminders(self):
        """Create automatic reminders for the reservation"""
        try:
            # 24-hour reminder
            reminder_24h = self.start_time - timedelta(hours=24)
            if reminder_24h > timezone.now():
                Reminder.objects.create(
                    reservation=self,
                    reminder_time=reminder_24h,
                    reminder_type='24h',
                    message=f"Reminder: Your reservation '{self.title}' is tomorrow at {self.start_time.strftime('%H:%M')}"
                )
            
            # 1-hour reminder
            reminder_1h = self.start_time - timedelta(hours=1)
            if reminder_1h > timezone.now():
                Reminder.objects.create(
                    reservation=self,
                    reminder_time=reminder_1h,
                    reminder_type='1h',
                    message=f"Reminder: Your reservation '{self.title}' starts in 1 hour at {self.start_time.strftime('%H:%M')}"
                )
            
            # 15-minute reminder
            reminder_15m = self.start_time - timedelta(minutes=15)
            if reminder_15m > timezone.now():
                Reminder.objects.create(
                    reservation=self,
                    reminder_time=reminder_15m,
                    reminder_type='15m',
                    message=f"Final reminder: Your reservation '{self.title}' starts in 15 minutes!"
                )
                
        except Exception as e:
            logger.error(f"Error creating reminders for reservation {self.id}: {e}")

    def send_confirmation_email(self):
        """Send email confirmation for the reservation"""
        try:
            subject = f"Reservation Confirmed: {self.title}"
            message = f"""
Hello {self.user.get_full_name() or self.user.username},

Your room reservation has been confirmed:

Room: {self.room.name}
Date: {self.start_time.strftime('%B %d, %Y')}
Time: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}
Title: {self.title}
Description: {self.description}

You will receive automatic reminders before your meeting.

Thank you for using our conference room booking system!

Best regards,
Conference Room Booking System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )
            
            logger.info(f"Confirmation email sent for reservation {self.id}")
            
        except Exception as e:
            logger.error(f"Error sending confirmation email for reservation {self.id}: {e}")

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds() / 3600

    @property
    def is_past(self):
        return self.end_time < timezone.now()

    @property
    def is_current(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('reservation_confirmed', 'Reservation Confirmed'),
        ('reservation_cancelled', 'Reservation Cancelled'),
        ('reservation_reminder', 'Reservation Reminder'),
        ('reservation_updated', 'Reservation Updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}"


class Reminder(models.Model):
    REMINDER_TYPES = [
        ('24h', '24 Hours Before'),
        ('1h', '1 Hour Before'),
        ('15m', '15 Minutes Before'),
        ('email', 'Email Reminder'),
    ]
    
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.DateTimeField()
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPES)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['reminder_time']
    
    def __str__(self):
        return f"{self.reservation.title} - {self.get_reminder_type_display()}"
    
    def send_reminder(self):
        """Send the reminder notification and email"""
        try:
            # Create notification
            Notification.objects.create(
                user=self.reservation.user,
                notification_type='reminder',
                title=f"Meeting Reminder: {self.reservation.title}",
                message=self.message,
                related_reservation=self.reservation
            )
            
            # Send email reminder
            subject = f"Meeting Reminder: {self.reservation.title}"
            email_message = f"""
Hello {self.reservation.user.get_full_name() or self.reservation.user.username},

{self.message}

Meeting Details:
Room: {self.reservation.room.name}
Date: {self.reservation.start_time.strftime('%B %d, %Y')}
Time: {self.reservation.start_time.strftime('%H:%M')} - {self.reservation.end_time.strftime('%H:%M')}
Title: {self.reservation.title}

Please arrive on time for your meeting.

Best regards,
Conference Room Booking System
            """
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [self.reservation.user.email],
                fail_silently=False,
            )
            
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save()
            
            logger.info(f"Reminder sent for reservation {self.reservation.id}")
            
        except Exception as e:
            logger.error(f"Error sending reminder {self.id}: {e}")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username