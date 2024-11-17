from django import forms
from .models import LandProperty , Location

class LandPropertyForm(forms.ModelForm):
    class Meta:
        model = LandProperty
        fields = ['name']  # Only allow editing of the name field

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['village', 'parish', 'sub_county', 'county', 'district', 'country']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = LandProperty
        fields = ['name', 'PID', 'size', 'valuation']