# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 1.1
from scrapy import signals
from scrapy.exporters import CsvItemExporter

# 1.2
from models import MediumDbModel, create_table, db_connect
from sqlalchemy.orm import sessionmaker

# class MediumScraperPipeline:
#     def process_item(self, item, spider):
#         return item



# ################################################################
# ######################  Spider 1.2   ###########################
# ################################################################


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
        Save real estate index in the database
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
        # catalog.published_date = item["published_date"]
        catalog.day = item["day"]
        catalog.month = item["month"]
        catalog.year = item["year"]

        try:
            print('Entry added')
            session.add(catalog)
            session.commit()
            # settings.saved = settings.saved + 1
            # settings.redundancy_streak = 0
        except:
            print('rollback')
            session.rollback()
            raise
        finally:
            session.close()
        
        return item

# ################################################################
# ######################  Spider 1.1   ###########################
# ################################################################

class CsvWriterPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('output.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
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
        # item.setdefault('published_date', None)
        item.setdefault('day', None)
        item.setdefault('month', None)
        item.setdefault('year', None)
 
        return item