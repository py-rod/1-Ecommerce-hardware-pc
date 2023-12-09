from django.shortcuts import render, redirect
from .form import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

# ACTIVATE EMAIL OR USER ACCOUNT
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token

# MESSAGES
from django.contrib import messages

# DEFAULT DECORATORS
from django.contrib.auth.decorators import login_required

# CUSTOM DECORATORS
from .decorators import user_not_authenticated

# AUTHENTICATED USER
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def activate_email(request, user, to_email):
    mail_sub = "Activate your user account"
    message = render_to_string("activate_account.html", {
        "user": user,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.id)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_sub, message, to=[to_email])
    if email.send():
        messages.success(request, "Check your email to verifications")
    else:
        messages.error(
            request, f"Problen sending confirm email {to_email}, check if your type it correctly")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activate")
        return redirect("signin")

    else:
        messages.error(request, "Activate link is invalid")
    return redirect("home")


@user_not_authenticated
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            activate_email(request, user, form.cleaned_data.get("email"))
            return redirect("home")
        else:
            for error in list(form.errors.values()).pop():

                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {
        "form": form
    })


@user_not_authenticated
def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Hi! Welcome {user.get_full_name()}")
                return redirect("home")
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
    else:
        form = AuthenticationForm()
    return render(request, "signin.html", {
        "form": form
    })


@login_required(login_url="signin")
def close_session(request):
    logout(request)
    messages.info(request, "You have logged out")
    return redirect("home")
