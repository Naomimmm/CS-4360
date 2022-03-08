import requests 
from bs4 import BeautifulSoup
import csv

target_path = '../static/images/books/'

with open('books.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        url = row[6]
        isbn = row[1]
        request = requests.get(url)
        if request.status_code == 200:
            with open(target_path + isbn + '.jpg', 'wb') as file:
                file.write(request.content)