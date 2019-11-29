# Products Crawler



## Introduction

A web crawler built with [scrapy](https://scrapy.org/) to crawl e-commerce and drop-shipping websites for products.

The initial motivation was to collect products and their images for building a "Visual Recommender Engine" for an e-commerce app, now I intend on extending the number of spiders to crawl more websites and provide more data resources.



About the crawler:

- The crawler uses [splash](https://github.com/scrapy-plugins/scrapy-splash) to wait for AJAX requests and load the data.
- MongoDB Pipeline is added to store the crawled products
- Custom Image Pipeline stores the crawled products' images locally in directories based on the categories



## Installation

1. First clone the repository:

   ` git clone https://github.com/YazanShannak/Products-Crawler.git`

2. Setup a virtual environment with venv (Optional):

   `python3 -m venv venv`

3. Install the required packages:

   `pip install -r requirements.txt`

4. Start scrapy splash with Docker:

   `docker container run -d -p 8050:8050 --name splash scrapinghub/splash:latest`

5. Start MongoDB (with Docker optionally):

   `docker container run -d -p 27017:27017 --name crawler_db mongo:latest`

6. Change directory to 'products_crawler':

   `cd products_crawler`

7. Run quotes_test spider for testing:

   `scrapy crawl quotes_test`

8. Run [Ubuy-JO](https://www.jordan.ubuy.com/en/) crawler:

   `scrapy crawl ubuy`



## Todo

- [ ] Docker Image and docker-compose for the crawler
- [ ] Cleanup pipelines
- [ ] Custom ImagePipeline for S3 (Custom Naming)
- [ ] Add more sites