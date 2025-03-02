from django import forms
from apps.transport.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'pickup_location', 'dropoff_location']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
