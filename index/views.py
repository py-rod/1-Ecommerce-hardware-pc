from django.shortcuts import render
from .models import Carousel
from django.utils import timezone
from datetime import timedelta
from products.models import Product
# Create your views here.


def index(request):
    images_carousel = Carousel.objects.filter(
        series__is_active=True, series__stock__gt=0)
    images_carousel = list(enumerate(images_carousel))
    date_now = timezone.now() - timedelta(days=30)
    recent_products = Product.objects.filter(
        series__is_active=True, is_active=True, stock__gt=0, created__gte=date_now)

    return render(request, "index.html", {
        "images_carousel": images_carousel,
        "recent_products": recent_products
    })
