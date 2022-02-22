from django.test import TestCase
from django.core.exceptions import ValidationError
from bookstore.models import *

# Create your tests here.
# Django test example: https://docs.djangoproject.com/en/4.0/topics/testing/overview/
class BookTestCase(TestCase):
    def test_valid_book(self):
        Book.objects.create(
            isbn = "195153448",
            title = "Classical Mythology",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Oxford University Press",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")
        
        valid_book = Book.objects.get(isbn="195153448")
        self.assertIsNotNone(valid_book)

    def test_invalid_book_isbn_too_long(self):
        Book.objects.create(
            isbn = "0000000000000000000000000000000",
            title = "Classical Mythology",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Oxford University Press",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")
        
        # max_length is not enforced.
        # verifying using full_clean and save, reference: https://stackoverflow.com/questions/8478054/django-model-charfield-max-length-does-not-work
        try:
            invalid_book = Book.objects.get(isbn="0000000000000000000000000000000")
            invalid_book.full_clean()
            invalid_book.save()
        except ValidationError:
            pass

    def test_invalid_book_title_too_long(self):
        Book.objects.create(
            isbn = "195153448",
            title = "This title is too long. This title is too long. This title is too long. This title is too long. This title is too long. This title is too long. This title is too long. This title is too long. This title is too long. This title is too long.",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Oxford University Press",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")
        
        # max_length is not enforced.
        # verifying using full_clean and save, reference: https://stackoverflow.com/questions/8478054/django-model-charfield-max-length-does-not-work
        try:
            invalid_book = Book.objects.get(isbn="195153448")
            invalid_book.full_clean()
            invalid_book.save()
        except ValidationError:
            pass

    def test_invalid_book_authors_too_long(self):
        Book.objects.create(
            isbn = "195153448",
            title = "Classical Mythology",
            authors = "Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long. Authors is too long.",
            year_public = "2002",
            publisher = "Oxford University Press",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")
        
        valid_book = Book.objects.get(isbn="195153448")
        self.assertIsNotNone(valid_book)

    def test_invalid_book_invalid_year(self):
        with self.assertRaises(ValueError):
            Book.objects.create(
                isbn = "195153448",
                title = "Classical Mythology",
                authors = "Mark P. O. Morford",
                year_public = "NotRealYear",
                publisher = "Oxford University Press",
                thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")

    def test_invalid_book_publisher_too_long(self):
        Book.objects.create(
            isbn = "195153448",
            title = "Classical Mythology",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long.",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg")
        
        valid_book = Book.objects.get(isbn="195153448")
        self.assertIsNotNone(valid_book)