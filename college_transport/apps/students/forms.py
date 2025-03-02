from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.html import strip_tags
from apps.transport.models import Booking, Bus
import bleach
import logging

logger = logging.getLogger(__name__)

class BookingForm(forms.ModelForm):
    bus = forms.ModelChoiceField(
        queryset=Bus.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select rounded-lg',
            'required': 'required'
        })
    )
    
    # Add validators for location fields
    location_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\s\-\.,#]{3,100}$',
        message='Location must be between 3 and 100 characters and contain only letters, numbers, spaces, and basic punctuation.'
    )
    
    pickup_location = forms.CharField(
        max_length=100,
        validators=[location_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-lg',
            'placeholder': 'Enter pickup location'
        })
    )
    
    dropoff_location = forms.CharField(
        max_length=100,
        validators=[location_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-lg',
            'placeholder': 'Enter drop-off location'
        })
    )
    
    class Meta:
        model = Booking
        fields = ['bus', 'date', 'pickup_location', 'dropoff_location']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-input rounded-lg',
                    'min': timezone.now().date().isoformat(),
                    'required': 'required'
                }
            )
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            # Check if date is not too far in the future (e.g., 30 days)
            max_future_date = timezone.now().date() + timezone.timedelta(days=30)
            if date < timezone.now().date():
                raise ValidationError("Booking date cannot be in the past")
            elif date > max_future_date:
                raise ValidationError("Booking date cannot be more than 30 days in the future")
        return date

    def clean_pickup_location(self):
        location = self.cleaned_data.get('pickup_location')
        if location:
            # Sanitize input
            location = bleach.clean(location, tags=[], strip=True)
            location = strip_tags(location)
            location = location.strip()
            if len(location) < 3:
                raise ValidationError("Pickup location must be at least 3 characters long")
        return location

    def clean_dropoff_location(self):
        location = self.cleaned_data.get('dropoff_location')
        if location:
            # Sanitize input
            location = bleach.clean(location, tags=[], strip=True)
            location = strip_tags(location)
            location = location.strip()
            if len(location) < 3:
                raise ValidationError("Drop-off location must be at least 3 characters long")
        return location

    def clean(self):
        try:
            cleaned_data = super().clean()
            bus = cleaned_data.get('bus')
            date = cleaned_data.get('date')
            pickup = cleaned_data.get('pickup_location')
            dropoff = cleaned_data.get('dropoff_location')
            
            if bus and date:
                # Check if bus is available on that date
                existing_bookings = Booking.objects.filter(
                    bus=bus,
                    date=date,
                    status='confirmed'
                ).count()
                
                if existing_bookings >= bus.capacity:
                    raise ValidationError("This bus is fully booked for the selected date")
                
                # Check if user already has a booking for this date
                user_bookings = Booking.objects.filter(
                    student=self.instance.student if self.instance else None,
                    date=date,
                    status='confirmed'
                ).exists()
                
                if user_bookings:
                    raise ValidationError("You already have a booking for this date")
                
                # Validate pickup and dropoff locations are different
                if pickup and dropoff and pickup.lower() == dropoff.lower():
                    raise ValidationError("Pickup and drop-off locations cannot be the same")
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error in booking form validation: {str(e)}")
            raise ValidationError("An error occurred while processing your booking. Please try again.")
