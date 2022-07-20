import requests
from bs4 import BeautifulSoup
import pprint
import json


def parse(region):
    domain = 'https://youtravel.me'
    region_search = f'/tours/region/{region}'
    url = f'{domain}{region_search}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    info_for_bot = []
    result_for_bot = {}
    result = {}
    tours = soup.find_all('a', class_="tours-item__title")
    for tour_a in tours:
        text = tour_a.text
        result_for_bot['title'] = text.replace("\n", "")
        href = tour_a.get('href')
        url = f'{domain}{href}'
        result_for_bot['link'] = url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        info_for_bot.append((result_for_bot['title'], result_for_bot['link']))

        data = {}
        data["Подробно о туре: "] = url

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

    return info_for_bot


if __name__ == "__main__":
    region = input("Введите название интересующего региона (латинский алфавит): ")
    result = parse(region)
    pprint.pprint(result)
