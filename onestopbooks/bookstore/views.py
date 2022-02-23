from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def books_view(request, *args, **kwargs):
    return render(request, "products.html", {})

def aboutus_view(request, *args, **kwargs):
    return render(request, "aboutus.html", {})

def cart_view(request, *args, **kwargs):
    return render(request, "cart.html", {})
