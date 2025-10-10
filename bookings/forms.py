from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'location', 'description', 'amenities', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room name'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Floor 2, Building A'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the room features and purpose'
            }),
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'List available amenities (e.g., Projector, Whiteboard, Video Conferencing)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity < 1:
            raise forms.ValidationError("Capacity must be at least 1.")
        if capacity and capacity > 100:
            raise forms.ValidationError("Capacity cannot exceed 100.")
        return capacity

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check if room name already exists (excluding current instance)
            existing_rooms = Room.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing_rooms = existing_rooms.exclude(pk=self.instance.pk)
            if existing_rooms.exists():
                raise forms.ValidationError("A room with this name already exists.")
        return name