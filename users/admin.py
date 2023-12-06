from django.contrib import admin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active",
                    "is_staff", "is_superuser")
    list_display_links = ("id", "username", "email")
    list_filter = ("is_active", "is_staff", "is_superuser", "recive_notify")
    list_editable = ("is_active", "is_staff", "is_superuser")
    search_fields = ("id", "username", "email")
    list_per_page = 20
