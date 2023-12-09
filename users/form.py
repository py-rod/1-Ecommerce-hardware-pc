from typing import Any
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class UserCreationForm(UserCreationForm):
    class Meta:

        model = get_user_model()
        fields = ["first_name", "last_name", "username",
                  "email", "password1", "password2", "recive_notify"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.recive_notify = self.cleaned_data["recive_notify"]
        if commit:
            user.save()
        return user


class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.EmailInput(
        attrs={"type": "email", "autocomplete": "email", "autofocus": True}))
