import scrapy

class AmpSpider(scrapy.Spider):
    name = 'amp'
    allowed_domains = ['www.knowtheorigin.com']
    start_urls = ['https://knowtheorigin.com/collections/brands']

    def parse(self, response):
        links = response.xpath("//span[@class='btn btn-secondary collection-a-z__title']/text()")
        for link in links:
            yield{
                'name': link.get()
            }