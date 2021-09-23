import scrapy
from datetime import datetime
from decimal import Decimal

class ArticleSpider(scrapy.Spider):
    name = "medium_spider_basic"
    start_urls = ['https://medium.com/iearn/archive']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ROBOTSTXT_OBEY': True,
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

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
                published_date = datetime(year, month, day)

                article_url = article.xpath('.//a[contains(@class, "button--smaller")]/@href').get().split('?')[0]

                scraped_date = datetime.now()

                yield {
                    'author': author,
                    'title': title,
                    'subtitle preview': subtitle_preview,
                    'collection': collection,
                    'read time': int_read_time,
                    'claps': claps,
                    'responses': responses,
                    'published_date': published_date,
                    'article_url' : article_url,
                    'scraped_date': scraped_date
                }


def text_to_num(text):
    d = {'K': 3}
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return int(Decimal(num) * 10 ** d[magnitude])
    else:
        return int(Decimal(text))
