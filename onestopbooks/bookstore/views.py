import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from bookstore.models import *
from .forms import *

GENRE_PRODUCTS_HTML = "genre-products.html"

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def randombooks_view(request, *args, **kwargs):
    items = list(Book.objects.all())
    random_items = random.sample(items, 20)

    return render(request, GENRE_PRODUCTS_HTML, {'books': random_items})


def booksunder_view(request, *args, **kwargs):
    items_under = Book.objects.filter(price__range=(0, 9))
    items_under_sorted = items_under.order_by('price')

    return render(request, GENRE_PRODUCTS_HTML, {'books': items_under_sorted})


def newestbooks_view(request, *args, **kwargs):
    items_num = len(Book.objects.all())
    last_twenty = Book.objects.filter().order_by()[items_num-20:]

    return render(request, GENRE_PRODUCTS_HTML, {'books': last_twenty})


def books_view(request, *args, **kwargs):
    results = request.POST.get('book-filterd')

    if results == 'featured':
        books = Book.objects.all()
    elif results == 'titles_az':
        books = Book.objects.all().order_by('title')
    elif results == 'authors_az':
        books = Book.objects.all().order_by('authors')
    elif results == 'price_lh':
        books = Book.objects.all().order_by('price')
    elif results == 'price_hl':
        books = Book.objects.all().order_by('-price')
    else:
        books = Book.objects.all()

    return render(request, "products.html", {'books': books})


def aboutus_view(request, *args, **kwargs):
    return render(request, "aboutus.html", {})


def checkout_view(request, *args, **kwargs):
    return render(request, "checkout.html", {})


def cart_view(request, *args, **kwargs):
    return render(request, "cart.html", {})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'login.html',context)


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=createuserform()
        cust_form=createcustomerform()
        if request.method=='POST':
            form=createuserform(request.POST)
            cust_form=createcustomerform(request.POST)
            if form.is_valid() and cust_form.is_valid():
                user=form.save()
                customer=cust_form.save(commit=False)
                customer.user=user 
                customer.save()
                return redirect('login')
        context={
            'form':form,
            'cust_form':cust_form,
        }
        return render(request,'signup.html',context)


def logoutPage(request):
    logout(request)
    return redirect('/')


def product_view(request, isbn):
    book = Book.objects.get(isbn = isbn)
    return render(request, "product.html", {'book': book})

