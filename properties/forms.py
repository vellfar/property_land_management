from django import forms
from .models import LandProperty

class LandPropertyForm(forms.ModelForm):
    class Meta:
        model = LandProperty
        fields = ['name']  # Only allow editing of the name field
