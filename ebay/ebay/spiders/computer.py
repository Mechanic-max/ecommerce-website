import scrapy


class ComputerSpider(scrapy.Spider):
    name = 'computer'
    allowed_domains = ['www.ebay.co']
    start_urls = ['http://www.ebay.co.uk/b/Laptops-Netbooks/175672/bn_1631140?listingOnly=1/']

    def parse(self, response):
        links = response.xpath("//div[@class='s-item__wrapper clearfix']//a[@class='s-item__link']/@href")
        next_page = response.xpath("//a[@rel='next']/@href").get()
        for link in links:
            yield{
                'link':link.get(),
                'next_page':next_page
            }
