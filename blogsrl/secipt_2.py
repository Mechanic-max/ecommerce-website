import time
from scrapy.selector import Selector
import csv
import re
import pandas as pd
import datetime
import requests
import json
import xlsxwriter

class Serviceseeking():
    count = 0
    
        

    
    def target_url(self,url):
        html = requests.get(url).content
        resp = Selector(text=html)
        data =  resp.xpath("//li[@class='category']/a[@class='dropdown-item' and @data-depth='0']/@href").getall()
        for dat in data:
            print("Current Catagory >>>>>>>>>>> ",dat)
            time.sleep(1)
            self.next_page(dat)

    

                
    def next_page(self,url):
        time.sleep(2)
        html = requests.get(url).content
        resp = Selector(text=html)
        print("Current Page Scraping >>>>>>>>>>> ",url)
        self.result_scrap(resp)
        next_page_check = resp.xpath("//a[@rel='next']/@href").get()
        print(next_page_check)
        if next_page_check:
            self.next_page(next_page_check)
        else:
            print("Else Chala")
            None

    def result_scrap(self,resp):
        data = resp.xpath("//h3[@class='h3 product-title title-big']/a/@href").getall()
        for dat in data:
            results = str(dat)
            print("Current Product Scraping >>>>>>>>>>> ",results)
            with open("links.csv",'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([results])
            
            


    def scrap(self,link):
        self.driver.get(link)
        time.sleep(4)
        html = self.driver.page_source
        resp = Selector(text=html)
        
        
        barcode = resp.xpath("normalize-space(//dt[contains(text(),'Barcode')]/following-sibling::dd[1]/text())").extract_first()
        price_per_item = resp.xpath("normalize-space(//p[@class='product-unit-price sub']/text())").extract_first()
        price_per_box = resp.xpath("normalize-space(//span[@class='unit' and contains(text(),'(per carton)')]/preceding-sibling::span[1]/text())").extract_first()
        scraped_links = link
        
        print()
        print("barcode:",barcode) #A
        print("price_per_item:",price_per_item) #B
        print("price_per_box:",price_per_box) #C
        print("scraped_links:",scraped_links) #D
        print()
        
        try:
            self.df = pd.read_excel("Dataset.xls")
        except Exception as e:
            self.df = pd.DataFrame({
                'Barcode': [], 
                'Price per Item': [],
                'Price per Cart':[],
                'Scraped Link':[]
            })
            print(e)
        
        item = {'Barcode': barcode, 'Price per Item': price_per_item,'Price per Cart':price_per_box,'Scraped Link':scraped_links}

        self.df = self.df.append(item , ignore_index=True)
        self.df.to_excel("Dataset.xls", index=False)

        self.count = self.count + 1
        print("Data saved in CSV: ",self.count)         
                    

if __name__ == '__main__':
    urls = [
        "https://blogsrl.it/gb/",
    ]
    
    scraper = Serviceseeking()
    for url in urls:
        scraper.target_url(url)
