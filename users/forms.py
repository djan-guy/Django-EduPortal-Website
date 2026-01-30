from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password1', 'password2', 'firstName', 'lastName', 'dateOfBirth', 'address']
    dateOfBirth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))