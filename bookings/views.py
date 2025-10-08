from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Room, Reservation, Notification, UserProfile
from .forms import (
    CustomUserCreationForm, UserProfileForm, ReservationForm, 
    ReservationUpdateForm, RoomSearchForm, AdminReservationForm
)


def home(request):
    """Home page with available rooms overview"""
    rooms = Room.objects.filter(is_active=True)[:6]
    upcoming_reservations = []
    
    if request.user.is_authenticated:
        upcoming_reservations = Reservation.objects.filter(
            user=request.user,
            start_time__gte=timezone.now(),
            status='confirmed'
        ).order_by('start_time')[:5]
    
    context = {
        'rooms': rooms,
        'upcoming_reservations': upcoming_reservations,
    }
    return render(request, 'bookings/home.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


@login_required
def room_list(request):
    """List all available rooms with search functionality"""
    form = RoomSearchForm(request.GET)
    rooms = Room.objects.filter(is_active=True)
    
    if form.is_valid():
        capacity = form.cleaned_data.get('capacity')
        date = form.cleaned_data.get('date')
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')
        
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        
        if date and start_time and end_time:
            # Combine date and time
            start_datetime = timezone.make_aware(datetime.combine(date, start_time))
            end_datetime = timezone.make_aware(datetime.combine(date, end_time))
            
            # Filter rooms that are available during the specified time
            available_rooms = []
            for room in rooms:
                if room.is_available(start_datetime, end_datetime):
                    available_rooms.append(room)
            rooms = available_rooms
    
    paginator = Paginator(rooms, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'bookings/room_list.html', context)


@login_required
def room_detail(request, room_id):
    """Room detail view with booking form"""
    room = get_object_or_404(Room, id=room_id, is_active=True)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                reservation=reservation,
                notification_type='reservation_confirmed',
                message=f'Your reservation for {room.name} has been confirmed for {reservation.start_time.strftime("%Y-%m-%d %H:%M")}.'
            )
            
            messages.success(request, 'Reservation created successfully!')
            return redirect('reservation_detail', reservation.id)
    else:
        form = ReservationForm(user=request.user)
    
    # Get upcoming reservations for this room
    upcoming_reservations = Reservation.objects.filter(
        room=room,
        start_time__gte=timezone.now(),
        status='confirmed'
    ).order_by('start_time')[:10]
    
    context = {
        'room': room,
        'form': form,
        'upcoming_reservations': upcoming_reservations,
    }
    return render(request, 'bookings/room_detail.html', context)


@login_required
def reservation_list(request):
    """User's reservation list"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-start_time')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        reservations = reservations.filter(status=status)
    
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
    }
    return render(request, 'bookings/reservation_list.html', context)


@login_required
def reservation_detail(request, reservation_id):
    """Reservation detail view"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'bookings/reservation_detail.html', {'reservation': reservation})


@login_required
def reservation_update(request, reservation_id):
    """Update reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.status == 'cancelled':
        messages.error(request, 'Cannot update a cancelled reservation.')
        return redirect('reservation_detail', reservation.id)
    
    if request.method == 'POST':
        form = ReservationUpdateForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                reservation=reservation,
                notification_type='reservation_updated',
                message=f'Your reservation for {reservation.room.name} has been updated.'
            )
            
            messages.success(request, 'Reservation updated successfully!')
            return redirect('reservation_detail', reservation.id)
    else:
        form = ReservationUpdateForm(instance=reservation)
    
    return render(request, 'bookings/reservation_update.html', {
        'form': form,
        'reservation': reservation
    })


@login_required
def reservation_cancel(request, reservation_id):
    """Cancel reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.status == 'cancelled':
        messages.error(request, 'Reservation is already cancelled.')
        return redirect('reservation_detail', reservation.id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            reservation=reservation,
            notification_type='reservation_cancelled',
            message=f'Your reservation for {reservation.room.name} has been cancelled.'
        )
        
        messages.success(request, 'Reservation cancelled successfully!')
        return redirect('reservation_list')
    
    return render(request, 'bookings/reservation_cancel.html', {'reservation': reservation})


@login_required
def profile(request):
    """User profile view and edit"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'bookings/profile.html', {'form': form, 'profile': profile})


@login_required
def notifications(request):
    """User notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read
    notifications.update(is_read=True)
    
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/notifications.html', {'page_obj': page_obj})


# Admin views
@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Statistics
    total_rooms = Room.objects.filter(is_active=True).count()
    total_reservations = Reservation.objects.count()
    active_reservations = Reservation.objects.filter(status='confirmed').count()
    total_users = User.objects.count()
    
    # Recent reservations
    recent_reservations = Reservation.objects.order_by('-created_at')[:10]
    
    # Upcoming reservations
    upcoming_reservations = Reservation.objects.filter(
        start_time__gte=timezone.now(),
        status='confirmed'
    ).order_by('start_time')[:10]
    
    context = {
        'total_rooms': total_rooms,
        'total_reservations': total_reservations,
        'active_reservations': active_reservations,
        'total_users': total_users,
        'recent_reservations': recent_reservations,
        'upcoming_reservations': upcoming_reservations,
    }
    return render(request, 'bookings/admin_dashboard.html', context)


@login_required
def admin_room_manage(request):
    """Admin room management"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    rooms = Room.objects.all().order_by('name')
    return render(request, 'bookings/admin_room_manage.html', {'rooms': rooms})


@login_required
def admin_reservation_manage(request):
    """Admin reservation management"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    reservations = Reservation.objects.all().order_by('-start_time')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        reservations = reservations.filter(status=status)
    
    paginator = Paginator(reservations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
    }
    return render(request, 'bookings/admin_reservation_manage.html', context)


@login_required
def admin_reservation_create(request):
    """Admin create reservation for any user"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AdminReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.created_by_admin = True
            reservation.save()
            
            # Create notification for the user
            Notification.objects.create(
                user=reservation.user,
                reservation=reservation,
                notification_type='reservation_confirmed',
                message=f'A reservation for {reservation.room.name} has been created for you by an administrator.'
            )
            
            messages.success(request, 'Reservation created successfully!')
            return redirect('admin_reservation_manage')
    else:
        form = AdminReservationForm()
    
    return render(request, 'bookings/admin_reservation_create.html', {'form': form})


@login_required
def admin_reservation_cancel(request, reservation_id):
    """Admin cancel any reservation"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        
        # Create notification for the user
        Notification.objects.create(
            user=reservation.user,
            reservation=reservation,
            notification_type='reservation_cancelled',
            message=f'Your reservation for {reservation.room.name} has been cancelled by an administrator.'
        )
        
        messages.success(request, 'Reservation cancelled successfully!')
        return redirect('admin_reservation_manage')
    
    return render(request, 'bookings/admin_reservation_cancel.html', {'reservation': reservation})


# API views for AJAX
@login_required
def check_room_availability(request, room_id):
    """Check room availability for given time period"""
    room = get_object_or_404(Room, id=room_id)
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    
    if not start_time or not end_time:
        return JsonResponse({'available': False, 'error': 'Missing time parameters'})
    
    try:
        start_dt = timezone.make_aware(datetime.fromisoformat(start_time))
        end_dt = timezone.make_aware(datetime.fromisoformat(end_time))
        
        available = room.is_available(start_dt, end_dt)
        return JsonResponse({'available': available})
    except ValueError:
        return JsonResponse({'available': False, 'error': 'Invalid time format'})