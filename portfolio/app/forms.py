from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    """
    Form for editing User model fields
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for editing UserProfile model fields
    """
    # Custom field for location input (latitude and longitude separately)
    latitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Latitude (e.g., 40.7128)',
            'step': 'any'
        }),
        help_text='Latitude coordinate'
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Longitude (e.g., -74.0060)',
            'step': 'any'
        }),
        help_text='Longitude coordinate'
    )
    
    class Meta:
        model = UserProfile
        fields = ['home_address', 'phone_number']
        widgets = {
            'home_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full home address',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1-555-123-4567'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate latitude and longitude if location exists
        if self.instance and self.instance.location:
            self.fields['latitude'].initial = self.instance.location.y
            self.fields['longitude'].initial = self.instance.location.x
    
    def save(self, commit=True):
        """
        Override save to handle location Point creation from lat/lng
        """
        instance = super().save(commit=False)
        
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')
        
        if latitude is not None and longitude is not None:
            from django.contrib.gis.geos import Point
            instance.location = Point(longitude, latitude)
        elif latitude is None and longitude is None:
            instance.location = None
        
        if commit:
            instance.save()
        return instance

