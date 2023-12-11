from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import CustomUser
# FORMS
from .form import UserCreationForm, AuthenticationForm, SetPasswordForm, UpdateProfile
from django.contrib.auth.forms import PasswordResetForm
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

# CART
from cart.models import Cart, CartItem
from cart.views import _cart_id
# ORDERS
from orders.models import Order, Payment, OrderProduct
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
                # PASS ALL THE PRODUCTS THAT WERE ADDED TO THE CART, BEFORE AUTHENTICATION
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))

                    is_cart_item_exists = CartItem.objects.filter(
                        cart=cart).exists()

                    if is_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)

                        for item in cart_items:
                            existing_item = CartItem.objects.filter(
                                user=user, product=item.product).first()
                            if existing_item:
                                existing_item.quantity += item.quantity
                                existing_item.save()
                            else:
                                item.user = user
                                item.save()
                except Cart.DoesNotExist:
                    pass

                login(request, user)
                messages.success(request, f"Welcome {user.get_full_name()}")
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


@user_not_authenticated
def forogot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user_associated = get_user_model().objects.filter(Q(email=email)).first()
            if user_associated:
                subjet = "Password Reset request"
                message = render_to_string("forgot_password.html", {
                    "user": user_associated,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(user_associated.id)),
                    "token": account_activation_token.make_token(user_associated),
                    "protocol": "https" if request.is_secure() else "http"
                })
                email = EmailMessage(subjet, message, to=[
                                     user_associated.email])
                if email.send():
                    messages.success(
                        request, "Check your email for reset password")
                    return redirect("home")
    else:
        form = PasswordResetForm()
    return render(request, "forgot_password_reset_form.html", {
        "form": form,
        "type": "reset"
    })


@user_not_authenticated
def reset_password_validate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Enter the new password")
        return redirect("reset_password_confirm")
    else:
        messages.error(request, "The link has been expired")
        return redirect("signin")


@user_not_authenticated
def password_reset_confirm(request):
    if request.method == "POST":
        uid = request.session.get("uid")
        user = get_user_model().objects.get(id=uid)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your password has been set, enter the new password for sign in")
            return redirect("signin")
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
    else:
        form = SetPasswordForm(user)
    return render(request, "forgot_password_reset_form.html", {
        "form": form,
        "type": "confirm",
    })


@login_required(login_url="signin")
def profile(request):
    if request.method == "POST":
        form = UpdateProfile(request.POST, request.FILES,
                             instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated")
            return redirect(request.path)
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
    else:
        form = UpdateProfile(instance=request.user)
    return render(request, "profile.html", {
        "form": form,
    })


@login_required(login_url="signin")
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been change")
            return redirect("signin")
        else:
            for error in list(form.errors.values()).pop():
                messages.error(request, error)
    else:
        form = SetPasswordForm(user)
    return render(request, "change_password.html", {
        "form": form
    })


@login_required(login_url="signin")
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by("-created")
    return render(request, "my_orders.html", {
        "orders": orders
    })


@login_required(login_url="signin")
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    return render(request, "order_detail.html", {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal
    })
