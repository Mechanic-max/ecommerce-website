import scrapy
import wget
# coding: 'utf-8'

class SamSpider(scrapy.Spider):
    name = 'sam'
    allowed_domains = ['www.nord-ex.com']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.nord-ex.com/Catalog/Adhesives/?feature=17,11',callback=self.parse_item,dont_filter=True)

    
    def parse_item(self, response):
        pdf_nam,msds_nam,im="","",""
        pdf_name=response.xpath("(//div[@class='pifd_files td']/a)[2]/@href").extract_first()
        msds_name = response.xpath("(//div[@class='pifd_files td']/a)[1]/@href").extract_first()
        img = response.xpath("//div[@id='product_img']//@src").extract_first()
        catagory = response.xpath("(//a[@itemprop='url']/span[@itemprop='title'])[3]/text()").extract_first()
        if img:
            wget.download(img,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            try:
                im = ""
                im = img
                im = im.replace("https://www.nord-ex.com/images/Products/",'')
            except:
                im = ""
                im = img    
                im = im.replace("https://www.nord-ex.com.il/images/",'')
        if pdf_name:
            wget.download(pdf_name,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            pdf_nam = ""
            pdf_nam = pdf_name
            pdf_nam = pdf_nam.replace('https://www.nord-ex.com/images/Products/files/',"")
            
            
        if msds_name:
            wget.download(msds_name,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            msds_nam = ""
            msds_nam = msds_name
            msds_nam = msds_nam.replace("https://www.nord-ex.com/images/Products/files/","")
            

        cat =""
        cat_no = response.xpath("(//div[@class='prod_desc']/strong/text())[1]").extract_first()
        cat = cat_no
        cat = cat.replace('Catalog Number:','')
        cat = cat.lstrip()
        desc = response.xpath("normalize-space(//div[@class='sub_title']/text())").extract_first()
        yield{
            'url':response.url,
            'Item name (Title H1)':response.xpath("//div[@class='page_title td']/h1/text()").get(),
            'Catalog Number':cat,
            'Description Item in category':desc,
            'Friendly URL':response.xpath("//meta[@name='description']/@content").extract_first(),
            'Title':response.xpath("//title[contains(text(),' ')]/text()").extract_first(), #
            'Description':response.xpath("//meta[@name='description']/@content").extract_first(),
            'Keywords':response.xpath("//meta[@name='keywords']/@content").extract_first(),
            'Price':response.xpath("//div[@class='pil_price']/strong/text()").extract_first(),
            'Image':im,
            'PDF':pdf_nam,
            'MSDS':msds_nam,
            'Catagories':catagory,
            'Brand':response.xpath("//div[@class='td img']/img/@alt").extract_first(),
            'Features':response.xpath("//div[@class='features']/div/img/@title").getall()
        }
