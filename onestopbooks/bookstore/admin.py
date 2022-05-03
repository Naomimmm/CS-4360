from django.contrib import admin
from .models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    """ Search for Book Model in AdminPage where Admin can search a book by using 
    isbn, title, authors, year public, and publisher of that book """
    
    search_fields = ('isbn', 'title', 'authors', 'year_public', 'publisher',)

class CustomerAdmin(admin.ModelAdmin):
    """ Search for Customer in AdminPage where Admin can search for a customer by using 
    first name, last name, email, phone number of that customer """
    
    search_fields = ('first_name', 'last_name', 'email', 'phone_number',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(RentItem)
admin.site.register(ReviewRating)
