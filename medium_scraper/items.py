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
    if text != None:
        return text.split()[0]

def getPublishedDate(published_date):
    try:
        date_object = datetime.strptime(published_date, "%b %d, %Y")
        year = date_object.year
    except:
        date_object = datetime.strptime(published_date, "%b %d")
        year = datetime.now().year
    day = date_object.day
    month = date_object.month
    formatted_published_date = datetime(year, month, day)
    return formatted_published_date


def getArticleUrl(raw_url):
    if raw_url != None:
        return raw_url.split('?')[0]


class MediumScraperItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    subtitle_preview = scrapy.Field()
    collection = scrapy.Field()
    read_time = scrapy.Field(input_processor=MapCompose(getNumericReadTime))
    claps = scrapy.Field(input_processor=MapCompose(text_to_num))
    responses = scrapy.Field(input_processor=MapCompose(getNumericResponse))
    published_date = scrapy.Field(input_processor=MapCompose(getPublishedDate))
    article_url = scrapy.Field(input_processor=MapCompose(getArticleUrl))
    scraped_date = scrapy.Field()
