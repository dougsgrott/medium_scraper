# Medium Scraper

Medium Scraper is a scrapy project intended to scrape overview data from Medium's publication archive.

You can run the code from this repository or directly access the scraped public data.

## Description

The goal of this project is to scrape data from the Medium website using Scrapy, a powerful and flexible web scraping framework.

The scraped public data can be saved in csv, json or SQLite format and can be used for various purposes such as organizing study material, analytics, see trends throughout time, data analysis and visualization or building machine learning models.

## Data Overview

The data consists of the following columns:
- author
- title
- subtitle_preview
- collection
- read_time
- claps
- responses
- published_date
- article_url
- scraped_date

The public data scraped from X Publications are described in the table below:

|             Publication          |  Number of articles  | Number of authors |   Starting date   |     End date     |
|:--------------------------------:|:--------------------:|:-----------------:|:-----------------:|:----------------:|
| TDS Archive                      |          60773       |       13483       |     2013-10-10    |    2025-02-03    |
| bitgrit Data Science Publication |          133         |       11          |     2018-11-21    |    2024-09-24    |



## Installation

To run this project, you need to have Python and Scrapy installed on your system. You can install Scrapy using pip:

```
pip install scrapy
```

## Usage

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Modify the Scrapy spider to specify the websites you want to scrape and the data you want to extract.
4. Run the Scrapy spider using the following command:

```
scrapy crawl <spider_name>
```

Replace `<spider_name>` with the name of your Scrapy spider.

## Configuration

You can configure various settings for your Scrapy project in the `settings.py` file. This includes settings such as user agents, download delays, and pipelines for processing scraped data.

## How to collect data

The web scraper is designed to scrape articles from a publication archive. To scrape the data, currently you need to pass the publication archive url as the `starting_url` argument on the `crawl` command from `spider_sqlitepipe.py`. Other ways to start the spider will be developed soon.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
