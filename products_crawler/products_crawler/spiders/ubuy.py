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
    return {url = splash:url(),
        html = splash:html()}

end
"""

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
        self.logger.info('Found {} items in the page'.format(len(items)))
        for item in items:
            url = item.xpath(".//h3[@class='product-name']/a/@href").extract_first()
            yield SplashRequest(url=url, callback=self.parse_item, endpoint='render.html', args={'lua_source' : lua_product_script})



    def parse_item(self, response):
        details = response.xpath(".//div[@class='product-details']")
        name = details.xpath(".//h2[@class='product-name']/text()").extract_first()
        name = self.parse_text(name)
        vendor = details.xpath(".//div[@class='brandname']/span/a/text()").extract_first()
        vendor = self.parse_text(vendor)
        price = details.xpath(".//h3[@class='product-price']/text()").extract_first()
        price = self.parse_price(price)
        item = ProductItem(name=name, vendor=vendor, price=price)
        if name != None:
            return item
        else:
            pass




    def parse_text(self, text):
        try:
            return re.sub('s/^\s+|\s+$|\s+(?=\s)', '', text)
        except:
            self.logger.warning('Invalid Entry {}'.format(text))


    def parse_price(self, price):
        try:
            return re.findall('\d+', price)[0]
        except:
            self.logger.warning('Invalid Entry {}'.format(price))