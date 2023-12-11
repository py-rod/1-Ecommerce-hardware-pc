from django.urls import path
from . import views


urlpatterns = [
    path("<slug:slug_category>/<slug:slug_product>",
         views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),

]
