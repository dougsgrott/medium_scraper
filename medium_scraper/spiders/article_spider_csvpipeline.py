import sys
sys.path.append("/home/user/PythonProj/medium_scraper/medium_scraper")

from scrapy.spiders import Spider
from scrapy import Request
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from items import MediumScraperItem
from datetime import datetime

# necessary to run the spider by executing this script
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ArticleSpider(Spider):
    name = "medium_spider_pipeline"
    start_urls = ['https://medium.com/iearn/archive']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'medium_scraper.pipelines.DefaultValuesPipeline': 1,
            'medium_scraper.pipelines.CsvWriterPipeline': 2,
        },
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
        item_loader.add_xpath('title', './/h3[contains(@class, "title")]/text()')
        item_loader.add_xpath('subtitle_preview', './/h4[@name="previewSubtitle"]/text()')
        item_loader.add_xpath('collection', './/a[@data-action="show-collection-card"]/text()')
        item_loader.add_xpath('read_time', './/*[@class="readingTime"]/@title')
        item_loader.add_xpath('claps', './/button[@data-action="show-recommends"]/text()')
        item_loader.add_xpath('responses', './/a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()')
        item_loader.add_xpath('published_date', './/time/text()')
        item_loader.add_xpath('article_url', './/a[contains(@class, "button--smaller")]/@href')
        item_loader.add_value('scraped_date', datetime.now())

        return item_loader.load_item()


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArticleSpider)
    process.start()
