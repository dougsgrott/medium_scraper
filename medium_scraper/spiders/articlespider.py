import scrapy
from scrapy.crawler import CrawlerProcess

import datetime
import requests
import lxml.html as parser

class ArticleSpider(scrapy.Spider):
    name = "medium"

    def start_requests(self):
        urls = [
            'https://medium.com/python-in-plain-english/archive',
            #'https://medium.com/iearn/archive',
            #'https://towardsdatascience.com/archive',
        ]
        #year_element = #/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]
        #month_element = #/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[3]
        #day_element = #/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[4]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')

        year_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/*/a/@href').getall()
        if len(year_pages) != 0:
            yield from response.follow_all(year_pages, callback=self.parse_months)
    
    def parse_months(self, response):
        month_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[3]/div/a/@href').getall()
        if len(month_pages) != 0:
            yield from response.follow_all(month_pages, callback=self.parse_days)
        else:
            self.parse_articles(response)

    def parse_days(self, response):
        day_pages = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[4]/div/a/@href').getall()
        if len(day_pages) != 0:
            yield from response.follow_all(day_pages, callback=self.parse_articles)
    
    def parse_articles(self, response):
        articles = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/*')
        if len(articles) != 0:
            for article in articles:
                author = article.xpath('.//a[@data-action="show-user-card"]/text()').get()
                published_date = article.xpath('.//time/text()').get()
                min_read = article.xpath('.//*[@class="readingTime"]/@title')[0].get()
                collection = article.xpath('.//a[@data-action="show-collection-card"]/text()').get()
                title = article.xpath('.//h3[contains(@class, "title")]/text()').get()
                try:
                    claps = article.xpath('.//button[@data-action="show-recommends"]/text()').get()
                except:
                    claps = 0
                try:
                    responses = article.xpath('.//a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()').get()
                except:
                    responses = 0
                try:
                    subtitle_preview = article.xpath('.//h4[@name="previewSubtitle"]/text()').get()
                except:
                    subtitle_preview = None
                yield {
                    'author' : author,
                    'title' : title,
                    'subtitle preview' : subtitle_preview,
                    'published date' : published_date,
                    'min read time' : min_read,
                    'collection' : collection,
                    'claps' : claps,
                    'responses' : responses
                }


# process = CrawlerProcess()
# process.crawl(ArticleSpider)
# process.start()



# url = "https://towardsdatascience.com/archive"
# response = requests.get(url, verify = False)
# parser = parser.fromstring(response.text)

#parser.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/*/a/@href')
