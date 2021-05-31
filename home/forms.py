from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy


class SignUpForm(UserCreationForm):
    name = forms.CharField(label=("Full Name"))
    username = forms.CharField(label=("Username"))
    email = forms.EmailField(label=('Email'))

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("The given email is already registered")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')
