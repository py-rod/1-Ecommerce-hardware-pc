from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = ("id", "product_name", "series", "is_active")
    list_display_links = ("id", "product_name")
    list_filter = ("series", "is_active")
    list_editable = ("series", "is_active")
    list_per_page = 20
    search_fields = ("id", "product_name", "series")
