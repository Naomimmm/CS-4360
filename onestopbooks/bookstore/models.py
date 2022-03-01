from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(_("isbn"), max_length = 30)
    title = models.CharField(_("title"), max_length = 100)
    authors = models.CharField(_("authors"), max_length = 100)
    year_public = models.IntegerField(_("year_public"), null = True)
    publisher = models.CharField(_("publisher"), max_length = 100, null = True)
    thumbnail_pic = models.ImageField(_("thumbnail_pic"), null = True, blank = True, upload_to ="static/images/books")

    def __str__(self):
        """String for representing the Book title."""
        return self.title

# Customer Model
class Customer(models.Model):
    """A customer model to store basic identifying information for customer end users."""

    # Fields
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    phone_number = models.IntegerField()
    address_1 = models.CharField(_("address"), max_length = 128)
    address_2 = models.CharField(_("address continued"), max_length = 128, blank=True)
    city = models.CharField(max_length = 128)
    state = models.CharField(max_length = 128)
    zip_code = models.CharField(max_length = 5) 