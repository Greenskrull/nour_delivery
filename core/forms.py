from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control bg-secondary text-light'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
