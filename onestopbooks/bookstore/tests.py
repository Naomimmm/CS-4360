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
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
            quantity = 10,
            price = 10)
        
        valid_book = Book.objects.get(isbn="195153448")
        self.assertIsNotNone(valid_book)

    def test_invalid_book_isbn_too_long(self):
        Book.objects.create(
            isbn = "0000000000000000000000000000000",
            title = "Classical Mythology",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Oxford University Press",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
            quantity = 10,
            price = 10)
        
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
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
            quantity = 10,
            price = 10)
        
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
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
            quantity = 10,
            price = 10)
        
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
                thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
                quantity = 10,
                price = 10)

    def test_invalid_book_publisher_too_long(self):
        Book.objects.create(
            isbn = "195153448",
            title = "Classical Mythology",
            authors = "Mark P. O. Morford",
            year_public = "2002",
            publisher = "Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long. Publisher too long.",
            thumbnail_pic = "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
            quantity = 10,
            price = 10)
        
        valid_book = Book.objects.get(isbn="195153448")
        self.assertIsNotNone(valid_book)

class CustomerTestCase(TestCase):
    def test_valid_customer(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "Denver",
            state = "Colorado",
            zip_code = "80123")

        valid_customer = Customer.objects.get(first_name="Amy")
        self.assertIsNotNone(valid_customer)

    def test_invalid_customer_name_too_long(self):
        Customer.objects.create(
            first_name = "AmyAmyAmyAmyAmyAmyAmyAmyAmyAmyAmy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "Denver",
            state = "Colorado",
            zip_code = "80123")

        try:
            invalid_customer = Customer.objects.get(first_name = "AmyAmyAmyAmyAmyAmyAmyAmyAmyAmyAmy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    def test_invalid_customer_last_name_too_long(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Last name is too long. Last name is too long.Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long. Last name is too long.",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "Denver",
            state = "Colorado",
            zip_code = "80123")

        try:
            invalid_customer = Customer.objects.get(first_name = "Amy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    def test_invalid_customer_invalid_address_1(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long. Address is too long.",
            city = "Denver",
            state = "Colorado",
            zip_code = "80123")

        try:
            invalid_customer = Customer.objects.get(first_name = "Amy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    def test_invalid_customer_invalid_city(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long. City is too long.",
            state = "Colorado",
            zip_code = "80123")

        try:
            invalid_customer = Customer.objects.get(first_name = "Amy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    def test_invalid_customer_invalid_state(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "Denver",
            state = "State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long. State is too long.",
            zip_code = "80123")

        try:
            invalid_customer = Customer.objects.get(first_name = "Amy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    def test_invalid_customer_invalid_zip_code(self):
        Customer.objects.create(
            first_name = "Amy",
            last_name = "Test",
            email = "AmyTest@gmail.com",
            address_1 = "123 S. Denver",
            city = "Denver",
            state = "Colorado",
            zip_code = "NoRealZipCode")

        try:
            invalid_customer = Customer.objects.get(first_name = "Amy")
            invalid_customer.full_clean()
            invalid_customer.save()
        except ValidationError:
            pass

    
    


            


    

    








