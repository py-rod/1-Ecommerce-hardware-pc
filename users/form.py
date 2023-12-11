from typing import Any
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
# RESET PASSWORD
from django.contrib.auth.forms import SetPasswordForm


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


# RESET PASSWORD OR FORGOT PASSWORD
class SetPasswordForm(SetPasswordForm):
    model = get_user_model()
    fields = ["new_password1", "new_password2"]


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["image", "username", "email", "first_name", "last_name", "city", "departament",
                  "address_city", "phone_number", "number_dui", "description"]

    def __init__(self, *args, **kwargs):
        super(UpdateProfile, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last name"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["email"].widget.attrs["readonly"] = True
        self.fields["city"].widget.attrs["placeholder"] = "City"
        self.fields["departament"].widget.attrs["placeholder"] = "Departament"
        self.fields["address_city"].widget.attrs["placeholder"] = "Address"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone number"
        self.fields["number_dui"].widget.attrs["placeholder"] = "Number DUI"
        self.fields["description"].widget.attrs["placeholder"] = "Description"
