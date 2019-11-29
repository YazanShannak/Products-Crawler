# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

lua_script = """
function main(splash)
    assert(splash:go(splash.args.url))

    while not splash:select('.quote') do
        splash:wait(0.1)
    end
    return {html = splash:html()}

end
"""


class QuotesTestSpider(scrapy.Spider):
    name = 'quotes_test'
    allowed_domains = ['quotes_test.com']
    start_urls = ['http://quotes.toscrape.com/js',]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'lua_source':lua_script}, meta={'name':'Hello'})

    def parse(self, response):
        self.logger.info(response.meta['name'])
        if response:
            quotes = response.xpath("//div[@class='quote']")
            for quote in quotes:
                text = quote.xpath("./span[@class='text']/text()").extract_first()
                yield {'quote': text }
        else:
            pass

