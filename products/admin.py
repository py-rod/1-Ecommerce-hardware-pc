from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["product_name", "slug", "series",  "image", "brand",  "stock", "price",
              "offer_price", "old_price", "percentage", "description", "is_active"]
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = ("id", "product_name", "series", "is_active")
    list_display_links = ("id", "product_name")
    list_filter = ("series", "is_active")
    list_editable = ("series", "is_active")
    list_per_page = 20
    search_fields = ("id", "product_name", "series")
    readonly_fields = ("old_price", "percentage")
