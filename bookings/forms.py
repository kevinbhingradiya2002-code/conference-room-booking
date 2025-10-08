from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Room, UserProfile
from django.utils import timezone
from datetime import datetime, timedelta


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'department']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter rooms to only show active ones
        self.fields['room'].queryset = Room.objects.filter(is_active=True)
        
        # Set minimum datetime to current time
        now = timezone.now()
        self.fields['start_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')
        self.fields['end_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = cleaned_data.get('room')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
            
            if start_time < timezone.now():
                raise forms.ValidationError("Cannot create reservation in the past.")
            
            # Check if room is available
            if room and not room.is_available(start_time, end_time):
                raise forms.ValidationError("Room is not available for the selected time period.")

        return cleaned_data


class ReservationUpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set minimum datetime to current time
        now = timezone.now()
        self.fields['start_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')
        self.fields['end_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
            
            if start_time < timezone.now():
                raise forms.ValidationError("Cannot create reservation in the past.")
            
            # Check if room is available (excluding current reservation)
            if not self.instance.room.is_available(start_time, end_time, self.instance):
                raise forms.ValidationError("Room is not available for the selected time period.")

        return cleaned_data


class RoomSearchForm(forms.Form):
    capacity = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Minimum capacity'})
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data


class AdminReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'user', 'title', 'description', 'start_time', 'end_time', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter rooms to only show active ones
        self.fields['room'].queryset = Room.objects.filter(is_active=True)
        
        # Set minimum datetime to current time
        now = timezone.now()
        self.fields['start_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')
        self.fields['end_time'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = cleaned_data.get('room')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
            
            if start_time < timezone.now():
                raise forms.ValidationError("Cannot create reservation in the past.")
            
            # Check if room is available (excluding current reservation if updating)
            if room and not room.is_available(start_time, end_time, self.instance if self.instance.pk else None):
                raise forms.ValidationError("Room is not available for the selected time period.")

        return cleaned_data
