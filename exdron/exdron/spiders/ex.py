import scrapy
import re
import string
from urllib.parse import unquote
import wget
# coding: 'utf-8'

class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = ['www.exdron.co.li']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.exdron.co.il/%D7%A7%D7%98%D7%9C%D7%95%D7%92/',callback=self.parse,dont_filter=True)

    def parse(self,response):
        links = response.xpath("(//div[@class='filtering_box'])[2]/div[@class='filtering_box_l']/div/a/@href")
        for link in links:
            yield scrapy.Request(url=link.get(),callback=self.second_page,dont_filter=True)
    
    def second_page(self,response):
        links = response.xpath("//section[@class='box']/a[@class='boxa']/@href")
        for link in links:
                yield scrapy.Request(url=link.get(),callback=self.third_page,dont_filter=True)
    
    def third_page(self,response):
        links = response.xpath("//h2[@class='pid_title']/a/@href")
        next_page = response.xpath("//div[@class='pagination_left']/a/@href").get()
        for link in links:
            yield scrapy.Request(url=link.get(),callback=self.parse_item,dont_filter=True)
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.third_page,dont_filter=True)
    
    def parse_item(self, response):
        pdf_nam,msds_nam,im="","",""
        pdf_name=response.xpath("(//div[@class='pifd_files td']/a)[2]/@href").extract_first()
        msds_name = response.xpath("(//div[@class='pifd_files td']/a)[1]/@href").extract_first()
        img = response.xpath("//div[@id='product_img']//@src").extract_first()
        catagory = response.xpath("(//a[@itemprop='url']/span[@itemprop='title'])[3]/text()").extract_first()
        if catagory:
            catagory = unquote(catagory)
        if img:
            wget.download(img,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            try:
                im = ""
                im = img
                im = im.replace("https://www.exdron.co.il/images/Products/",'')
            except:
                im = ""
                im = img    
                im = im.replace("https://www.exdron.co.il/images/",'')
        if pdf_name:
            wget.download(pdf_name,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            pdf_nam = ""
            pdf_nam = pdf_name
            pdf_nam = pdf_nam.replace('https://www.exdron.co.il/images/Products/files/',"")
            
            
        if msds_name:
            wget.download(msds_name,out='/Users/nabee/projects/e-commerence/exdron/exdron/spiders/result')
            msds_nam = ""
            msds_nam = msds_name
            msds_nam = msds_nam.replace("https://www.exdron.co.il/images/Products/files/","")
            

        cat =""
        cat_no = unquote(response.xpath("(//div[@class='prod_desc']/strong/text())[1]").extract_first())
        cat = cat_no
        cat = cat.replace('מק"ט:','')
        cat = cat.lstrip()
        desc = response.xpath("normalize-space(//div[@class='sub_title']/text())").extract_first()
        if desc:
            desc = unquote(desc)
        yield{
            'url':unquote(response.url),
            'Item name (Title H1)':response.xpath("//div[@class='page_title td']/h1/text()").get(),
            'Catalog Number':cat,
            'Description Item in category':desc,
            'Friendly URL':response.xpath("//meta[@name='description']/@content").extract_first(),
            'Title':response.xpath("//title[contains(text(),' ')]/text()").extract_first(), 
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
