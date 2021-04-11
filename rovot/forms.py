from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'register-input-username',
        'type': 'text',
    }), label='Username')

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'register-input-email',
        'type': 'text',
    }), label='Email')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'register-input-password',
        'type': 'password',
    }), label='Password')

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'register-input-confirm',
        'type': 'password',
    }), label='Confirm Password')

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']