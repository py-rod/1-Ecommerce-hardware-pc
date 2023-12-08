from django.contrib import admin
from .models import Carousel
# Register your models here.


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "series")
    list_display_links = ("id", "series")
    list_per_page = 20
    search_fields = ("id", "series")
