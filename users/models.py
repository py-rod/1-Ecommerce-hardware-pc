from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        # CREA Y DEVUELVE UN USUARIO CON LOS CAMPOS DADOS
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Profile_pick", self.email, instance)
        return None
    username = models.CharField(
        max_length=200, default="", blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=150, default="", blank=False)
    last_name = models.CharField(max_length=150, default="", blank=False)
    departament = models.CharField(blank=False, max_length=100)
    city = models.CharField(blank=False, max_length=100)
    address_city = models.CharField(blank=False, max_length=250)
    phone_number = models.CharField(max_length=50, default="", blank=False)
    number_dui = models.CharField(default="", max_length=9, blank=False)
    description = models.CharField(max_length=500, default="", blank=True)
    image = models.ImageField(
        default="./default/default_profile.webp", upload_to=image_upload_to)
    recive_notify = models.BooleanField(
        "Would you like to receive promotional emails?", default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"
        db_table = "Users"
        ordering = ("-id", )
