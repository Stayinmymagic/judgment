import scrapy


class JudgeSpider(scrapy.Spider):
    name = 'judge'
    allowed_domains = ['judgment.judicial.gov.tw']
    start_urls = ['http://judgment.judicial.gov.tw/']

    def parse(self, response):
        pass
