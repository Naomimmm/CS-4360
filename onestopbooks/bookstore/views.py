import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from bookstore.models import *
from .forms import *
from django.http import JsonResponse
import json
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

GENRE_PRODUCTS_HTML = "genre-products.html"
SUCCESS_CHECKOUT_HTML = "checkout-success.html"


# Create your views here.
def home_view(request, *args, **kwargs):
    """ Function to return home page """
    if request.user.is_authenticated:
        customer = request.user.customer
        buy, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = buy.orderitem_set.all()
                
    else: # for user that isnt log in
        items = [] # empty for now
        buy = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'buy':buy}
    return render(request, "home.html", context)


def successcheckout_view(request, *args, **kwargs):
    """ Function to display successful order message after checkout """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items_to_purchase = order.orderitem_set.all() # this is for purchase
        items_to_rent = order.rentitem_set.all() # this is for rent

        for item in items_to_purchase:
            item.product.decrease_quantity(item.quantity)

        for item in items_to_rent:
            item.product1.decrease_quantity(item.quantity1)

    return render(request, SUCCESS_CHECKOUT_HTML, {})


def randombooks_view(request, *args, **kwargs):
    """ Function to return 20 random books """
    items = list(Book.objects.all())
    random_items = random.sample(items, 20)

    return render(request, GENRE_PRODUCTS_HTML, {'books': random_items})


def booksunder_view(request, *args, **kwargs):
    """ Function to return book under $10 """
    items_under = Book.objects.filter(price__range=(0, 9))
    items_under_sorted = items_under.order_by('price')

    return render(request, GENRE_PRODUCTS_HTML, {'books': items_under_sorted})


def newestbooks_view(request, *args, **kwargs):
    """ Function to return 20 newest book """
    items_num = len(Book.objects.all())
    last_twenty = Book.objects.filter().order_by()[items_num-20:]

    return render(request, GENRE_PRODUCTS_HTML, {'books': last_twenty})

def books_view(request, *args, **kwargs):
    """ Function to return all of our books and also book filter """
    if request.user.is_authenticated:
        customer = request.user.customer
        buy, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = buy.orderitem_set.all() # this is for purchase
    else: # for user that isnt log in
        items = [] # empty for now
        buy = {'get_cart_total':0, 'get_cart_items':0}
    
    results = request.POST.get('book-filterd')
    
    books = Book.objects.all()
    p = Paginator(Book.objects.all(), 20)
    page = request.GET.get('page')
    book_page = p.get_page(page)   
        
    if results == 'titles_az':
        p = Paginator(Book.objects.all().order_by('title'), 20)
        book_page = p.get_page(page) 
        
    elif results == 'authors_az':
        p = Paginator(Book.objects.all().order_by('authors'), 20)
        book_page = p.get_page(page) 
        
    elif results == 'price_lh':
        p = Paginator(Book.objects.all().order_by('price'), 20)
        book_page = p.get_page(page) 
        
    elif results == 'price_hl':
        p = Paginator(Book.objects.all().order_by('-price'), 20)
        book_page = p.get_page(page) 
      
    context = {'items':items, 'buy':buy, 'books':books, 'book_page':book_page}

    return render(request, "products.html", context)

def aboutus_view(request, *args, **kwargs):
    """ Return about us page """
    if request.user.is_authenticated:
        customer = request.user.customer
        buy, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = buy.orderitem_set.all() # this is for purchase
    else: # for user that isnt log in
        items = [] # empty for now
        buy = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'buy':buy}
    return render(request, "aboutus.html", context)

def checkout_view(request, *args, **kwargs):
    """ Return checkout page """
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False) # create object or quere one, if object isnt exist then we will create it
        items = order.orderitem_set.all() # this is for purchase
    else: # for user that isnt log in
        items = [] # empty for now
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    
    return render(request, "checkout.html", context)

def cart_view(request, *args, **kwargs):
    """ Return cart page with 3 sections BUY and Rent and Total """
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
    """ For Return Customer to login to web page """
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
    """ For new user to register an account """
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
    """ Logout and return to homepage """
    logout(request)
    return redirect('/')

def product_view(request, isbn):
    """ Return invididual page for a book with book details """
    book = Book.objects.get(isbn = isbn)
    reviews = ReviewRating.objects.filter(book_id = book.isbn)
    context = {
        'book':book,
        'reviews': reviews,
    }
    return render(request, "product.html", context)

def update_item(request):
    """ Function to add book to Cart to Buy or Rent section depending on which button clicked """
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

def search_results(request):
    """ Function to return search result for books """
    if request.method == "POST":
        results = request.POST['searched']
        books = Book.objects.filter(Q(title__contains = results) | Q(isbn__contains = results) | Q(authors__contains = results) | Q(year_public__contains = results) | Q(publisher__contains = results))
        return render(request, "search.html", {'results': results, 'books': books})
    else:
        return render(request, "search.html", {})
    

def submit_review(request, book_isbn):
    """ To create/save review to dabase and return to same url """
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':        
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            data = ReviewRating()
            data.subject = form.cleaned_data['subject']
            data.rate = form.cleaned_data['rate']
            data.review = form.cleaned_data['review']
            data.book_id = book_isbn
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thank you! Your review has been submitted')
            return redirect(url)
