# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# from real estate
from itemloaders.processors import Compose, TakeFirst, Join, MapCompose
import re
from w3lib.html import remove_tags

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

# author = article.xpath('.//a[@data-action="show-user-card"]/text()').get()
                
# str_read_time = article.xpath('.//*[@class="readingTime"]/@title')[0].get()

# collection = article.xpath('.//a[@data-action="show-collection-card"]/text()').get()
# title = article.xpath('.//h3[contains(@class, "title")]/text()').get()

# claps = article.xpath('.//button[@data-action="show-recommends"]/text()').get()
# if claps == None:
#     claps = 0
# else:
#     claps = claps.split()[0]
# if type(claps) == str:
#     claps = text_to_num(claps)



# subtitle_preview = article.xpath('.//h4[@name="previewSubtitle"]/text()').get()

# published_date = article.xpath('.//time/text()').get()
# try:
#     date_object = datetime.strptime(published_date, "%b %d, %Y")
#     day = date_object.day
#     month = date_object.month
#     year = date_object.year
# except:
#     date_object = datetime.strptime(published_date, "%b %d")
#     day = date_object.day
#     month = date_object.month
#     year = datetime.now().year


class MediumScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # input_processor=cleanText
    # id = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    subtitle_preview = scrapy.Field()
    collection = scrapy.Field()
    read_time = scrapy.Field(input_processor=MapCompose(getNumericReadTime))
    claps = scrapy.Field(input_processor=MapCompose(text_to_num))
    responses = scrapy.Field(input_processor=MapCompose(getNumericResponse))
    # published_date = scrapy.Field()
    day = scrapy.Field(input_processor=MapCompose(getPublishedDay))
    month = scrapy.Field(input_processor=MapCompose(getPublishedMonth))
    year = scrapy.Field(input_processor=MapCompose(getPublishedYear))
    

# class ImoveisSCItem(scrapy.Item):
#     id = scrapy.Field()
#     title = scrapy.Field(input_processor=cleanText)
#     code = scrapy.Field(input_processor=cleanText)
#     price = scrapy.Field(input_processor=cleanText)
#     caracteristicas_simples = scrapy.Field()
#     description = scrapy.Field(input_processor=Compose(cleanText, Join(separator='<br>')))
#     caracteristicas_detalhes = scrapy.Field()
#     address = scrapy.Field(input_processor=cleanText)
#     advertiser = scrapy.Field()
#     advertiser_info = scrapy.Field(input_processor=MapCompose(remove_tags))
#     local = scrapy.Field(input_processor=MapCompose(getLocal))
#     business_type = scrapy.Field(input_processor=MapCompose(getBusinessType))
#     property_type = scrapy.Field(input_processor=MapCompose(getPropertyType))
#     #https://www.../governador-celso-ramos/comprar/sala-escritorio
#     url = scrapy.Field(output_processor=TakeFirst())
#     date = scrapy.Field(output_processor=TakeFirst())

    