import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from decimal import Decimal
from scrapy.utils.project import get_project_settings

class ArticleSpider(scrapy.Spider):
    name = "medium_basic"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 5,
        'ROBOTSTXT_OBEY': False,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    def start_requests(self):
        urls = [
            # 'https://towardsdatascience.com/archive'
            #'https://medium.com/python-in-plain-english/archive',
            'https://medium.com/iearn/archive',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        year_div = response.xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]")
        year_pages = year_div.xpath(".//a/@href").getall()
        if len(year_pages) != 0:
            yield from response.follow_all(year_pages, callback=self.parse_months)
        else:
            yield from self.parse_articles(response)
    
    def parse_months(self, response):
        month_div = response.xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[3]")
        month_pages = month_div.xpath(".//a/@href").getall()
        if len(month_pages) != 0:
            yield from response.follow_all(month_pages, callback=self.parse_days)
        else:
            yield from self.parse_articles(response)

    def parse_days(self, response):
        day_div = response.xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[4]")        
        day_pages = day_div.xpath(".//a/@href").getall()
        if len(day_pages) != 0:
            yield from response.follow_all(day_pages, callback=self.parse_articles)
        else:
            yield from self.parse_articles(response)
    
    def parse_articles(self, response):
        articles = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/*')
        if len(articles) != 0:
            for article in articles:
                author = article.xpath('.//a[@data-action="show-user-card"]/text()').get()
                
                str_read_time = article.xpath('.//*[@class="readingTime"]/@title')[0].get()
                int_read_time = str_read_time.split()[0]

                collection = article.xpath('.//a[@data-action="show-collection-card"]/text()').get()
                
                title = article.xpath('.//h3[contains(@class, "title")]/text()').get()
                
                claps = article.xpath('.//button[@data-action="show-recommends"]/text()').get()
                if claps != None:
                    claps = claps.split()[0]               
                    if type(claps) == str:
                        claps = text_to_num(claps)

                responses = article.xpath('.//a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()').get()
                if responses != None:
                    responses = responses.split()[0]
                
                subtitle_preview = article.xpath('.//h4[@name="previewSubtitle"]/text()').get()
                
                published_date = article.xpath('.//time/text()').get()
                try:
                    date_object = datetime.strptime(published_date, "%b %d, %Y")
                    year = date_object.year
                except:
                    date_object = datetime.strptime(published_date, "%b %d")
                    year = datetime.now().year
                day = date_object.day
                month = date_object.month

                yield {
                    'author' : author,
                    'title' : title,
                    'subtitle preview' : subtitle_preview,
                    'collection' : collection,
                    'read time' : int_read_time,
                    'claps' : claps,
                    'responses' : responses,
                    'day' : day,
                    'month' : month,
                    'year' : year
                }


def text_to_num(text):
    d = {'K': 3}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return int(Decimal(num) * 10 ** d[magnitude])
    else:
        return int(Decimal(text))

# if __name__ == '__main__':
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(ArticleSpider)
#     process.start()