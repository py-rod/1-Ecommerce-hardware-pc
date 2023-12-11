from django.shortcuts import render, redirect
from .models import Product, ReviewProduct
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from cart.models import CartItem
from cart.views import _cart_id
from orders.models import OrderProduct
from .form import ReviewForm
from django.contrib import messages

# Create your views here.


def product_detail(request, slug_category, slug_product):
    try:
        product = Product.objects.get(
            series__slug=slug_category, slug=slug_product,  is_active=True)
        # Implements to know if the product is added to cart
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=product).exists()

        reviews = ReviewProduct.objects.filter(product=product)

        # Procesar el formulario de comentarios si es una solicitud POST
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.product = product
                new_comment.user = request.user  # Asumiendo que tienes autenticación de usuario
                new_comment.save()
                return redirect(request.path)
        else:
            form = ReviewForm()

    except Exception as e:
        raise e

    return render(request, "product_detail.html", {
        "product": product,
        "in_cart": in_cart,
        "reviews": reviews,
        "title_window": product.product_name,
        "form": form
    })


def search(request):
    search_query = request.GET.get("q", "")
    page = request.GET.get("page")

    if search_query:
        products = Product.objects.filter(
            Q(product_name__icontains=search_query), series__is_active=True, is_active=True, stock__gt=0).order_by("price")

        paginator = Paginator(products, 1)
        try:
            products_post = paginator.page(page)
        except PageNotAnInteger:
            products_post = paginator.page(1)
        except EmptyPage:
            products_post = paginator.page(paginator.num_pages)
        return render(request, "search.html", {
            "products": products_post,
            "search_query": search_query,
        })
    else:
        return render(request, "search.html", {
            "products": False,
            "search_query": search_query,
        })
