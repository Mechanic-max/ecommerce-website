import scrapy


class SampleSpider(scrapy.Spider):
    name = 'sample'
    allowed_domains = ['www.auc.onejp.net']
    start_urls = ['http://auc.onejp.net/m?name=catalog&mnf_id=9&mdl_id=782']

    def parse(self, response):
        tables = response.xpath("//table[@class='tbl_cat']//tr[not(@style) and not(@class)]")
        for table in tables:
            yield{
                'Modification': table.xpath(".//td/a/text()").get(),
                'Chassis ID': table.xpath(".//td[2]//descendant::*/text()").extract(),
                'Engine': table.xpath(".//td[3]/text()").get(),
                'Drive': table.xpath(".//td[4]/text()").get()
            }
