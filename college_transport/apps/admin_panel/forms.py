from django import forms
from apps.transport.models import ServiceRecord  # Assuming you have a ServiceRecord model

class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['bus', 'service_date', 'details']  # Adjust fields as necessary
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-select'}),
            'service_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'details': forms.Textarea(attrs={'class': 'form-input'}),
        }
