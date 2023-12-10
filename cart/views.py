from django.shortcuts import render, redirect

# Create your views here.


def cart(request):
    return render(request, "cart.html")
