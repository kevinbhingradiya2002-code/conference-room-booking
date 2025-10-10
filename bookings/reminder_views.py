from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reminder, Reservation
from django.core.paginator import Paginator


@login_required
def reminder_list(request):
    """View all reminders for the current user"""
    reminders = Reminder.objects.filter(
        reservation__user=request.user
    ).order_by('-reminder_time')
    
    paginator = Paginator(reminders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'reminders': page_obj,
    }
    return render(request, 'bookings/reminder_list.html', context)


@login_required
def admin_reminder_manage(request):
    """Admin view to manage all reminders"""
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    reminders = Reminder.objects.all().order_by('-reminder_time')
    
    # Filter options
    reminder_type = request.GET.get('type')
    if reminder_type:
        reminders = reminders.filter(reminder_type=reminder_type)
    
    is_sent = request.GET.get('sent')
    if is_sent == 'true':
        reminders = reminders.filter(is_sent=True)
    elif is_sent == 'false':
        reminders = reminders.filter(is_sent=False)
    
    paginator = Paginator(reminders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'reminders': page_obj,
        'reminder_types': Reminder.REMINDER_TYPES,
    }
    return render(request, 'bookings/admin_reminder_manage.html', context)
