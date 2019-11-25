# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re


class UbuySpider(scrapy.Spider):
    name = 'ubuy'
    allowed_domains = ['jordan.ubuy.com']
    start_urls = ['http://jordan.ubuy.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_categories, endpoint='render.html')

    def parse_categories(self, response):
        categories = response.xpath('//div[@class="shop-by-menu-block"]/nav/ul/li/a/@href').extract()
        for category in categories:
            yield SplashRequest(category, callback=self.parse_category_items, endpoint='render.html' ,args={'wait': 1})

    def parse_category_items(self, response):
        items = response.xpath("//div[contains(@class, 'item-view')]")
        # items = response.xpath("//div[@class='item-view']")
        # items = response.xpath("//h3[@class='product-name']/a/text()").extract()
        self.logger.info('Found {} items in the page'.format(len(items)))
        for item in items:
            name = item.xpath(".//h3[@class='product-name']/a/text()").extract_first()
            name = re.sub('s/^\s+|\s+$|\s+(?=\s)', '', name)
            yield {'name': name}
