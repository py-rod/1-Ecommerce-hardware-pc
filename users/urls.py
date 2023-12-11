from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.close_session, name="logout"),
    # ACTIVATE ACCOUNT
    path("activate/<uidb64>/<token>", views.activate, name="activate"),

    # RESET PASSWORD
    # FORMTO SEND LINK FOR RESET PASSWORD
    path("forgot_password", views.forgot_password, name="forgot_password"),
    # VALIDATE RESET PASSWORD AND IF TRUE REDIRECT RESET_PASSWORD_CONFIRM
    path("reset_password_validate/<uidb64>/<token>", views.reset_password_validate,
         name="reset_password_validate"),
    # FORM TO RESET PASSWORD
    path("reset_password", views.password_reset_confirm,
         name="reset_password_confirm"),

    path("profile", views.profile, name="profile"),
    path("change_password", views.change_password, name="change_password"),
    path('my_orders/', views.my_orders, name='my_orders'),
    path("order_detail/<int:order_id>", views.order_detail, name="order_detail"),

]
