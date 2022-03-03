from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from bookstore.models import *

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def books_view(request, *args, **kwargs):
    books = Book.objects.all()
    return render(request, "products.html", {'books': books})

def aboutus_view(request, *args, **kwargs):
    return render(request, "aboutus.html", {})

def checkout_view(request, *args, **kwargs):
    return render(request, "checkout.html", {})

def cart_view(request, *args, **kwargs):
    return render(request, "cart.html", {})

def product_view(request, isbn):
    book = Book.objects.get(isbn = isbn)
    return render(request, "product.html", {'book': book})