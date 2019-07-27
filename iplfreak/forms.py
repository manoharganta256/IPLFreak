from django import forms
from django.contrib.auth.models import User
from iplfreak.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Enter username"
    }))

    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Enter Password'
    }))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Enter firstname'
    }))

    last_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Enter lastname'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Enter Email'
    }))

    username = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': "Enter username"
    }))

    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Enter Password'
    }))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'profile_picture')
