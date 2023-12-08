from django.shortcuts import render
from .models import Carousel
from django.utils import timezone
from datetime import datetime
# Create your views here.


def index(request):
    images_carousel = Carousel.objects.filter(
        series__is_active=True, series__stock__gt=0)
    images_carousel = list(enumerate(images_carousel))

    return render(request, "index.html", {
        "images_carousel": images_carousel
    })
