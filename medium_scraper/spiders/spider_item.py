from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

import sys
import os
curr_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.abspath(os.path.join(curr_path, os.pardir))
sys.path.append(base_path)
from items import MediumScraperItem

from datetime import datetime


class ArticleSpider(Spider):
    name = "spider_item"
    start_urls = ['https://medium.com/bitgrit-data-science-publication/archive/'] # https://towardsdatascience.com/archive # https://medium.com/hackernoon/archive
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': False,
        'FEED_EXPORT_FIELDS': ['author', 'title', 'subtitle_preview', 'collection', 'read_time', 'claps', 'responses', 'published_date', 'article_url', 'scraped_date']
    }
    
    def parse(self, response):
        year_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/*/a/@href').getall()
        if len(year_pages) != 0:
            yield from response.follow_all(year_pages, callback=self.parse_months)
        else:
            yield from self.parse_articles(response)
    

    def parse_months(self, response):
        month_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[3]/div/a/@href').getall()
        if len(month_pages) != 0:
            yield from response.follow_all(month_pages, callback=self.parse_days)
        else:
            yield from self.parse_articles(response)


    def parse_days(self, response):
        day_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[4]/div/a/@href').getall()
        if len(day_pages) != 0:
            yield from response.follow_all(day_pages, callback=self.parse_articles)
        else:
            yield from self.parse_articles(response)
    

    def parse_articles(self, response):
        articles = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/*')
        for article_selector in articles:
            yield self.populate_item(article_selector, response.url)


    def populate_item(self, selector, url):
        item_loader = ItemLoader(item=MediumScraperItem(), selector=selector)
        item_loader.default_output_processor = TakeFirst()
        item_loader.add_xpath('author', './/a[@data-action="show-user-card"]/text()')
        item_loader.add_xpath('title', './/*[contains(@class, "title")]/text()')
        item_loader.add_xpath('title', './/h3[contains(@class, "title")]/*/text()')
        item_loader.add_xpath('subtitle_preview', './/*[@name="previewSubtitle"]/text()')
        item_loader.add_xpath('collection', './/a[@data-action="show-collection-card"]/text()')
        item_loader.add_xpath('read_time', './/*[@class="readingTime"]/@title')
        item_loader.add_xpath('claps', './/button[@data-action="show-recommends"]/text()')
        item_loader.add_xpath('responses', './/a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()')
        item_loader.add_xpath('published_date', './/time/text()')
        item_loader.add_xpath('article_url', './/a[contains(@class, "button--smaller")]/@href')
        item_loader.add_value('scraped_date', datetime.now())

        return item_loader.load_item()

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(ArticleSpider)
    process.start()