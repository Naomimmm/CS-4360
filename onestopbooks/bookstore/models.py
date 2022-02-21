from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(_("isbn"), max_length = 30)
    title = models.CharField(_("title"), max_length = 100)
    authors = models.CharField(_("authors"), max_length = 100)
    year_public = models.IntegerField(_("year_public"), null = True)
    publisher = models.CharField(_("publisher"), max_length = 100, null = True)
    thumbnail_pic = models.ImageField(_("thumbnail_pic"), null = True, blank = True, upload_to ="images/")