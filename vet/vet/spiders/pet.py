import scrapy



class PetSpider(scrapy.Spider):
    li = input("Enter link which you want to scrape: ")
    li = str(li)
    name = 'pet'
    allowed_domains = ['www.aspcapetinsurance.com']
    start_urls = [li] #https://www.aspcapetinsurance.com/vet-locator/vet-clinics-by-state/?state=TN

    def parse(self, response):
        links =  response.xpath("//div[@class='col-md-3 col-xs-6']/p/a/@href")
        for link in links:
            absolute_url = response.urljoin(link.get())
            yield scrapy.Request(url=absolute_url,callback=self.parse_item)
    def parse_item(self,response):
        links =  response.xpath("//div[@class='col-md-4']")
        a=""
        for link in links:
            fax = link.xpath(".//span[@itemprop='faxNumber']/text()").get()
            if fax:
                a = fax
                a = a.replace('Fax:','')
            absolute_url = response.urljoin(link.xpath(".//div/a/@href").get())
            yield scrapy.Request(url=absolute_url,callback=self.scrape_item,meta={'fax':a})
    
    def scrape_item(self, response):
        yield{
            'Name': response.xpath("//div[@class='col-md-4']/h3/text()").get(),
            'Street Address':response.xpath("//span[@itemprop='streetAddress']/text()").get(),
            'Locality':response.xpath("//span[@itemprop='addressLocality']/text()").get(),
            'State':response.xpath("//span[@itemprop='addressRegion']/text()").get(),
            'Zip code':response.xpath("//span[@itemprop='postalCode']/text()").get(),
            'Telephone': response.xpath("//span[@itemprop='telephone']/text()").get(),
            'fax': response.meta['fax']
        }