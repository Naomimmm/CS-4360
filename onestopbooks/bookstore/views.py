from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from bookstore.models import *
from .forms import *
from django.http import JsonResponse
import json
from django.contrib import messages
# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})


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
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = order.orderitem_set.all() # this is for purchase
        rents = order.rentitem_set.all() # this is for rent
    else: # for user that isnt log in
        items = [] # empty for now
        rents = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'rents':rents, 'order':order}
    
    return render(request, "checkout.html", context)


def cart_view(request, *args, **kwargs):
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer

        buy, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        rent, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = buy.orderitem_set.all() # this is for purchase
        rents = rent.rentitem_set.all() # this is for rent
    else: # for user that isnt log in
        items = [] # empty for now
        rents = []
        buy = {'get_cart_total':0, 'get_cart_items':0}
        rent = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'rents':rents, 'buy':buy, 'rent':rent}
    return render(request, "cart.html", context)
    


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
        else:
            messages.info(request, 'Username Or Password is incorrect')
            
       context={}
       return render(request,'login.html',context)


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=CreateUserForm()
        cust_form=CustomerForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            cust_form=CustomerForm(request.POST)
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

def update_item(request):
    data = json.loads(request.body)
    book_isbn = data['bookIsbn']
    action = data['action']
    # print out action and isbn in command prompt just to test
    print('Action:', action)
    print('bookIsbn:', book_isbn)
    
    customer = request.user.customer
    product1 = Book.objects.get(isbn=book_isbn)
    order1, created = Order.objects.get_or_create(customer=customer, complete=False)    
    
    rent_item, created = RentItem.objects.get_or_create(order1 = order1, product1=product1)
    order_item, created = OrderItem.objects.get_or_create(order = order1, product=product1)
    
    if action == 'purchase':
        order_item.quantity = (order_item.quantity + 1)
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)    
    elif action == 'remove':
       order_item.quantity = (order_item.quantity - 1)    
    order_item.save()
    
    if action =='rent':
        rent_item.quantity1 = (rent_item.quantity1 + 1)
    rent_item.save()
    
    
    if action =='delete':
        order_item.delete() 
    if order_item.quantity <= 0:
        order_item.delete()
          
    if action =='deleteRent':
        rent_item.delete()    
    if rent_item.quantity1 <= 0:
        rent_item.delete()
    return JsonResponse('Item was added', safe=False)
