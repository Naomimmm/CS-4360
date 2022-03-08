import csv
from django.core.management import BaseCommand
from bookstore.models import Book
import random

class Command(BaseCommand):
    help = 'Load a books csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):

        path_to_images = './static/images/books/'
        image_name = ''
        prices = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14 ,15, 16, 17]

        path = kwargs['path']
        with open(path, 'rt') as file:
            reader = csv.reader(file)
            for row in reader:
                image_name = row[1] + '.jpg'
                Book.objects.create(
                    isbn = row[1],
                    title = row[2],
                    authors = row[3],
                    year_public = row[4],
                    publisher = row[5],
                    thumbnail_pic = path_to_images + image_name,
                    price = random.choice(prices),
                    quantity = 10,
                )