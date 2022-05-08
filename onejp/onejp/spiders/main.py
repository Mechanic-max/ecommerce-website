import scrapy


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.auc.onejp.net']
    start_urls = ['http://auc.onejp.net/catalog']

    def parse(self, response):
        links = response.xpath("//table[@class='aj_tbl_manuf_list']//tr/td[not(@style) and not(@class)]/div/a")
        for link in links:
            link_u = link.xpath(".//@href").get()
            name = link.xpath(".//text()").get()
            yield scrapy.Request(url=response.urljoin(link_u), callback=self.parse_item,dont_filter=True,meta={'name':name})
    def parse_item(self, response):
        links = response.xpath("//table[@class='aj_tbl_model_list']//tr/td[@class='aj_model_list_name']/div/a")
        for link in links:
            link_u = link.xpath(".//@href").get()
            response.urljoin(link_u)
            name = response.meta['name']
            yield scrapy.Request(url=response.urljoin(link_u), callback=self.parse_item_scrap,dont_filter=True,meta={'name':name})
    def parse_item_scrap(self, response):
        tables = response.xpath("//table[@class='tbl_cat']//tr[not(@style) and not(@class)]")
        for table in tables:
            yield{
                'name': response.meta['name'],
                'Modification': table.xpath(".//td/a/text()").get(),
                'Chassis ID': table.xpath(".//td[2]//descendant::*/text()").extract(),
                'Engine': table.xpath(".//td[3]/text()").get(),
                'Drive': table.xpath(".//td[4]/text()").get()
            }