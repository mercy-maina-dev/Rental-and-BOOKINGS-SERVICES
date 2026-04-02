# houses/forms.py

from django import forms
from .models import House


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['title', 'description', 'location',
                  'price', 'bedrooms', 'image', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'e.g. Cozy 2-Bedroom Apartment in Westlands',
            'description': 'Describe the house — amenities, surroundings, rules...',
            'location': 'e.g. Westlands, Nairobi',
            'price': 'Monthly rent in KES',
            'bedrooms': 'Number of bedrooms',
        }
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 4})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update(
                    {'class': 'form-control', 'accept': 'image/*'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]
            field.help_text = None


class HouseSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
                        'class': 'form-control form-control-lg',
                        'placeholder': 'Search by location or title...'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Min price'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Max price'}))
    bedrooms = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Bedrooms'}))
