# bookings/forms.py

from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})
        self.fields['end_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'})
        self.fields['message'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3,
                   'placeholder': 'Optional message to the landlord...'})
        self.fields['message'].required = False
        self.fields['start_date'].help_text = None
        self.fields['end_date'].help_text = None
        self.fields['message'].help_text = None

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')

        from django.utils import timezone
        today = timezone.now().date()

        if start and start < today:
            self.add_error('start_date', 'Start date cannot be in the past.')

        if start and end:
            if end <= start:
                self.add_error(
                    'end_date', 'End date must be after the start date.')

        return cleaned
