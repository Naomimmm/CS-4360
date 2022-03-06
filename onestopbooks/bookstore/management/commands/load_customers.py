import csv
from django.core.management import BaseCommand
from models import Book

class Command(BaseCommand):
    help = 'Load a questions csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as file:
            reader = csv.reader(file)
            for row in reader:
                Book.objects.create(
                    attr1=row[0],
                    attr2=row[1],
                )