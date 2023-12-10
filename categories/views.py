from django.shortcuts import render, redirect
from .models import Categories
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from products.models import Product
# Create your views here.


def products_by_category(request, category_slug):
    # OBTAIN SELECT FILTER IN FRONT
    order_param = request.GET.get("order", "default")
    # GET SLUG TO SHARE IN FRONT
    category = Categories.objects.get(slug=category_slug)
    # OBTAIN PAGE
    page = request.GET.get("page")

    # OPTIONS TO FILTER
    order_fields = {
        'default': 'created',
        'price_low_to_high': 'price',
        'price_high_to_low': '-price',
        'name_a_to_z': 'product_name',
        'name_z_to_a': '-product_name',
    }

    # GET PRODUCTS BY DIFFERENT PARAMS
    products = Product.objects.filter(
        series__slug=category_slug, series__is_active=True, is_active=True, stock__gt=0).order_by(order_fields.get(order_param, "created"))

    paginator = Paginator(products, 20)
    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    return render(request, "products_by_category.html", {
        "products": paged_products,
        "category_name": category,
        'order_param': order_param
    })
