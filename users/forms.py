from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Username"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Email"
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Whatsapp Number"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password"
    }))
    location = forms.ChoiceField(
        choices=User.LOCATION_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )
    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "location")