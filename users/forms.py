from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    nin = forms.CharField(max_length=15, required=True, label="National ID Number")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'nin', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')
        if User.objects.filter(nin=nin).exists():
            raise forms.ValidationError("National ID Number is already in use.")
        return nin
