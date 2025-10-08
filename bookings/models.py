from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class Room(models.Model):
    """Model representing a conference room"""
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    amenities = models.TextField(blank=True, help_text="Available amenities (e.g., projector, whiteboard, etc.)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

    def is_available(self, start_time, end_time, exclude_reservation=None):
        """Check if room is available for given time period"""
        reservations = self.reservations.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='confirmed'
        )
        if exclude_reservation:
            reservations = reservations.exclude(id=exclude_reservation.id)
        return not reservations.exists()


class Reservation(models.Model):
    """Model representing a room reservation"""
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
        """Validate reservation data"""
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        
        if self.start_time < timezone.now():
            raise ValidationError("Cannot create reservation in the past.")
        
        # Check if room is available
        if not self.room.is_available(self.start_time, self.end_time, self):
            raise ValidationError("Room is not available for the selected time period.")
        
        # Check if user has conflicting reservations
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
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Calculate reservation duration in hours"""
        return (self.end_time - self.start_time).total_seconds() / 3600

    @property
    def is_past(self):
        """Check if reservation is in the past"""
        return self.end_time < timezone.now()

    @property
    def is_current(self):
        """Check if reservation is currently active"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time


class Notification(models.Model):
    """Model for storing user notifications"""
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


class UserProfile(models.Model):
    """Extended user profile for additional information"""
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