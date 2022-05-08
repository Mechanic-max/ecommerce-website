import scrapy

class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['www.indeed.com']
    start_urls = [
        'https://www.indeed.com/jobs?q=engineer+or+manager&l=United+States&fromage=14&start=%s' % pg for pg in range(470,990,10)
    ]

    def start_requests(self):
        for url in self.start_urls: 
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    def parse(self, response):
        links = response.xpath("//div[@class='jobsearch-SerpJobCard unifiedRow row result']")
        for link in links:
            abc = link.xpath(".//h2/a/@href").get()
            tim = link.xpath(".//div//span[@class='date ']/text()").get()
            absolute_url = f"https://www.indeed.com{abc}"
            yield scrapy.Request(url=absolute_url,callback=self.parse_item,dont_filter=True,meta={'tim':tim})

        # next_page = response.xpath("//a[@aria-label='Next']/@href").get()
        # absol_next_page = f"https://www.indeed.com{next_page}"
        # if next_page:
        #     yield scrapy.Request(url=absol_next_page,callback=self.parse)

    def parse_item(self, response):
        yield{
            'Experience Level':response.xpath("//h1[@class='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title']/text()").get(),
            'Company_Name':response.xpath("//div[@class='icl-u-lg-mr--sm icl-u-xs-mr--xs']/a/text()").get(),
            'Location':response.xpath("(//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div)[2]/text()").get(),
            'Job Type':response.xpath("(//div[@class='jobsearch-JobDescriptionSection-sectionItem']/div)[3]/text()").get(),
            'Salary Estimate':response.xpath("//span[@class='icl-u-xs-mr--xs']/text()").get(),
            'Remote':response.xpath("(//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div)[3]/text()").get(),
            'Date Posted': response.meta['tim']
        }