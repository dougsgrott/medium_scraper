import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime


class ArticleSpider(scrapy.Spider):
    name = "medium_basic"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'DOWNLOAD_DELAY': 5,
        'ROBOTSTXT_OBEY': False,
    }
    def start_requests(self):
        urls = [
            # 'https://towardsdatascience.com/archive'
            #'https://medium.com/python-in-plain-english/archive',
            'https://medium.com/iearn/archive',
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
                if claps == None:
                    claps = 0
                responses = article.xpath('.//a[@class="button button--chromeless u-baseColor--buttonNormal"]/text()').get()
                if responses == None:
                    responses = 0
                subtitle_preview = article.xpath('.//h4[@name="previewSubtitle"]/text()').get()
                
                published_date = article.xpath('.//time/text()').get()
                try:
                    date_object = datetime.strptime(published_date, "%b %d, %Y")
                    day = date_object.day
                    month = date_object.month
                    year = date_object.year
                except:
                    date_object = datetime.strptime(published_date, "%b %d")
                    day = date_object.day
                    month = date_object.month
                    year = datetime.now().year

                yield {
                    'author' : author,
                    'title' : title,
                    'subtitle preview' : subtitle_preview,
                    'collection' : collection,
                    'read time' : int_read_time,
                    'claps' : claps,
                    'responses' : responses,
                    'published date' : published_date,
                    'day' : day,
                    'month' : month,
                    'year' : year
                }


# process = CrawlerProcess()
# process.crawl(ArticleSpider)
# process.start()



# url = "https://towardsdatascience.com/archive"
# response = requests.get(url, verify = False)
# parser = parser.fromstring(response.text)

#parser.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/*/a/@href')


# pre solution for year:
# year_div = response.xpath("/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]")
# year_num = len(year_div.xpath(".//a"))
# where year_num is the number of links to different years