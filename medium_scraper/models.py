from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, DateTime, Float, Boolean, Text, JSON
from scrapy.utils.project import get_project_settings

from sqlalchemy.orm import sessionmaker

from datetime import datetime

Base = declarative_base()

def db_connect():
    """
    ####Performs database connection using database settings from settings.py.
    ####Returns sqlaclchemy engine instance.
    """
    url = get_project_settings().get("CONNECTION_STRING")
    return create_engine(url)

def create_table(engine):
    Base.metadata.create_all(engine, checkfirst=True)


class MediumDbModel(Base):
    __tablename__ = "medium"

    id = Column(Integer, primary_key=True)
    author = Column(String(50))
    title = Column(String(100))
    subtitle_preview = Column(String(200))
    collection = Column(String(50))
    read_time = Column(Integer)
    claps = Column(Integer)
    responses = Column(Integer)
    published_date = Column(DateTime)
    article_url = Column(String(200))
    scraped_date = Column(DateTime)

