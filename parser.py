import requests
from bs4 import BeautifulSoup
import pprint
import json
from csv import DictWriter

i = input("Введите название интересующего региона (маленькие буквы кириллица): ")
domain = 'https://youtravel.me'
region = f'/tours/region/{i}'
url = f'{domain}{region}'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

result = {}
tours = soup.find_all('a', class_="tours-item__title")
for tour_a in tours:
    text = tour_a.text
    href = tour_a.get('href')
    url = f'{domain}{href}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    tour_tag_ul = soup.find_all("ul", class_="hashtag")
    titles = []
    for tour_tag in tour_tag_ul:
        titles.append(tour_tag.text.replace('\n', ''))
    data["Тип тура:"] = titles

    price_tag = soup.find("span", class_="js-booking-total-price")
    price_tour = []
    for price in price_tag:
        price_tour.append(price.text.replace('\xa0', ' '))
    data["Стоимость тура:"] = price_tour

    days_tag = soup.find("span", class_="js-booking-days")
    days_tour = []
    for days in days_tag:
        days_tour.append(days.text)
    data["Количество дней тура:"] = days_tour

    result[text] = data

FILE_NAME = "htmlparsing.json"
with open(FILE_NAME, 'w') as f:
    json.dump(result, f)


pprint.pprint(result)

