import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.us-proxy.org']
    start_urls = ['http://www.us-proxy.org/']

    def parse(self, response):
        pass
