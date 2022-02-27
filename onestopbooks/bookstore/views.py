from django.shortcuts import render
from django.views import generic

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def books_view(request, *args, **kwargs):
    return render(request, "products.html", {})

def aboutus_view(request, *args, **kwargs):
    return render(request, "aboutus.html", {})

def checkout_view(request, *args, **kwargs):
    return render(request, "checkout.html", {})

def cart_view(request, *args, **kwargs):
    return render(request, "cart.html", {})
