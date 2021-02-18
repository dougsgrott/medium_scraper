# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import MapCompose

from datetime import datetime
from decimal import Decimal


def text_to_num(text):
    d = {'K': 3}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return int(Decimal(num) * 10 ** d[magnitude])
    else:
        return int(Decimal(text))


def getNumericResponse(text):
    if text == None:
        responses = 0
    else:
        responses = text.split()[0]
    return responses


def getNumericReadTime(text):
    return text.split()[0]


def getPublishedDay(published_date):
    try:
        date_object = datetime.strptime(published_date, "%b %d, %Y")
    except:
        date_object = datetime.strptime(published_date, "%b %d")
    day = date_object.day
    return day


def getPublishedMonth(published_date):
    try:
        date_object = datetime.strptime(published_date, "%b %d, %Y")
    except:
        date_object = datetime.strptime(published_date, "%b %d")
    month = date_object.month
    return month


def getPublishedYear(published_date):
    try:
        date_object = datetime.strptime(published_date, "%b %d, %Y")
        year = date_object.year
    except:
        date_object = datetime.strptime(published_date, "%b %d")
        year = datetime.now().year
    return year


class MediumScraperItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    subtitle_preview = scrapy.Field()
    collection = scrapy.Field()
    read_time = scrapy.Field(input_processor=MapCompose(getNumericReadTime))
    claps = scrapy.Field(input_processor=MapCompose(text_to_num))
    responses = scrapy.Field(input_processor=MapCompose(getNumericResponse))
    day = scrapy.Field(input_processor=MapCompose(getPublishedDay))
    month = scrapy.Field(input_processor=MapCompose(getPublishedMonth))
    year = scrapy.Field(input_processor=MapCompose(getPublishedYear))
    