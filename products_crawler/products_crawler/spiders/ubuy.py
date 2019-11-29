# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import re
from ..items import ProductItem


lua_product_script = """
function main(splash)
    assert(splash:go(splash.args.url))

    while not splash:select('.product-details') do
        splash:wait(0.1)
    end
    return {html = splash:html()}
end
"""

lua_category_script = """
function main(splash)
    assert(splash:go(splash.args.url))

    while not splash:select('.item-view') do
        splash:wait(0.1)
    end
    return {html = splash:html()}
end
"""

lua_another_page_script = """
function main(splash)
    assert(splash:go(splash.args.url))
    
    while not splash:select("li[title='Next']") do
        splash:wait(0.1)
    end
    next_button = splash:select("li[title='Next']")
    next_button.mouse_click()
    splash:wait(0.5)
    
    while splash:select('.loader-spin-overlay-absolute.loading') do
        splash:wait(1)
    end
    return {html=splash:html()}
end
"""


class UbuySpider(scrapy.Spider):
    name = 'ubuy'
    allowed_domains = ['jordan.ubuy.com']
    start_urls = ['http://jordan.ubuy.com/']

    ignored_categories = []

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_categories, endpoint='render.html')

    def parse_categories(self, response):
        categories = response.xpath('//div[@class="shop-by-menu-block"]/nav/ul/li/a')
        for category in categories:
            url = category.xpath('./@href').extract_first()
            name = category.xpath('./@title').extract_first()
            for i in range(1, 35):
                page_url = '{}?page={}'.format(url, i+1)
                yield SplashRequest(page_url, callback=self.parse_category_items, endpoint='execute', args={'lua_source': lua_category_script}, meta={'category_name': name})

    def parse_category_items(self, response):
        category_name = response.meta['category_name']
        items = response.xpath("//div[contains(@class, 'item-view')]")
        self.logger.info('Found {} items in the page'.format(len(items)))
        for item in items:
            url = item.xpath(".//h3[@class='product-name']/a/@href").extract_first()
            yield SplashRequest(url=url, callback=self.parse_item, endpoint='execute', args={'lua_source': lua_product_script }, meta={'category_name':category_name} )

    def parse_item(self, response):
        category = response.meta['category_name']
        details = response.xpath("//div[@class='product-details']")
        name = details.xpath(".//h2[@class='product-name']/text()").extract_first()
        vendor = details.xpath(".//div[@class='brandname']/span/a/text()").extract_first()
        price = details.xpath(".//h3[@class='product-price']/text()").extract_first()
        image_urls = response.xpath("//div[@id='product-main-images']//div[@class='owl-item active']/li[@class='item']//img/@src").extract_first()
        item = ProductItem(name=name, vendor=vendor, price=price, image_urls=[image_urls], category=category)
        return item
