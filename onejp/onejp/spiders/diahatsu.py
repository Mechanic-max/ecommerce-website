import scrapy


class DiahatsuSpider(scrapy.Spider):
    name = 'diahatsu'
    allowed_domains = ['www.auc.onejp.net']
    start_urls = ['http://auc.onejp.net/m?name=catalog&mnf_id=9']

    def parse(self, response):
        links = response.xpath("//table[@class='aj_tbl_model_list']//tr/td[@class='aj_model_list_name']/div/a")
        for link in links:
            link_u = link.xpath(".//@href").get()
            response.urljoin(link_u)
            name = link.xpath(".//text()").get()
            yield scrapy.Request(url=response.urljoin(link_u), callback=self.parse_item,dont_filter=True,meta={'name':name})
    def parse_item(self, response):
        tables = response.xpath("//table[@class='tbl_cat']//tr[not(@style) and not(@class)]")
        for table in tables:
            yield{
                'name': response.meta['name'],
                'Modification': table.xpath(".//td/a/text()").get(),
                'Chassis ID': table.xpath(".//td[2]//descendant::*/text()").extract(),
                'Engine': table.xpath(".//td[3]/text()").get(),
                'Drive': table.xpath(".//td[4]/text()").get()
            }

            #//table[@class='aj_tbl_manuf_list']//tr/td[not(@style) and not(@class)]/div/a