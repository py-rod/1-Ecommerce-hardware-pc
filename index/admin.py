from django.contrib import admin
from .models import Carousel
# Register your models here.


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image")
    list_display_links = ("id", "image")
    list_per_page = 20
    search_fields = ("id", "image")
