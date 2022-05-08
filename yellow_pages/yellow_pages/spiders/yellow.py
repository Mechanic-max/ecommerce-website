import scrapy


class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['www.yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=distribution+centers&geo_location_terms=91203']

    def parse(self, response):
        links = response.xpath("//div[@class='v-card']//a[@class='business-name']/@href")
        next_page = response.xpath("//a[@class='next ajax-page']/@href").get()
        absolute_url = f"https://www.yellowpages.com{next_page}"
        for link in links:
            yield response.follow(url=link.get(),callback=self.parse_item)
        if next_page:
            yield scrapy.Request(url=absolute_url,callback=self.parse)


    def parse_item(self, response):
        yield{
            'Title': response.xpath("//div[@class='sales-info']/h1/text()").get(),
            'Catagory': response.xpath("//p[@class='cats']/a/text()").get(),
            'Phone No': response.xpath("//p[@class='phone']/text()").get(),
            'Address    ': response.xpath("//h2[@class='address']/text() | //h2/span/text()").getall(),
            'Map_location': response.xpath("//a[@class='directions small-btn']/@href").get(),
        }