# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter

from models import MediumDbModel, create_table, db_connect
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem


class AvoidDuplicatesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.factory = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.factory()
        exist_title = session.query(MediumDbModel).filter_by(title=item["title"]).first()
        if (exist_title is not None):
            raise DropItem("Duplicate item found: {}".format(item["title"]))
        else:
            return item


class SQLiteWriterPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.factory = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component
        """
        session = self.factory()
        catalog = MediumDbModel()
        catalog.author = item["author"]
        catalog.title = item["title"]
        catalog.subtitle_preview = item["subtitle_preview"]
        catalog.collection = item["collection"]
        catalog.read_time = item["read_time"]
        catalog.claps = item["claps"]
        catalog.responses = item["responses"]
        catalog.published_date = item['published_date']
        catalog.article_url = item["article_url"]
        catalog.scraped_date = item['scraped_date']

        try:
            print('Entry added')
            session.add(catalog)
            session.commit()
        except:
            print('rollback')
            session.rollback()
            raise
        finally:
            session.close()
        
        return item


class CsvWriterPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('./scraped_data/data_from_csvpipe.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        # The line below is optional, but makes sure that the data is saved in a customized order
        self.exporter.fields_to_export = ['author', 'title', 'subtitle_preview', 'collection', 'read_time', 'claps', 'responses', 'published_date', 'article_url', 'scraped_date']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item.setdefault('author', None)
        item.setdefault('title', None)
        item.setdefault('subtitle_preview', None)
        item.setdefault('collection', None)
        item.setdefault('read_time', None)
        item.setdefault('claps', None)
        item.setdefault('responses', None)
        item.setdefault('published_date', None)
        item.setdefault('article_url', None)
        item.setdefault('scraped_date', None)
 
        return item
