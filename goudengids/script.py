from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.support.ui import Select
import re
import pandas as pd
import datetime
import requests
import json
from datetime import date

class Serviceseeking():
    count = 0
    keyword = 'vastgoed '
    def start(self):
        options = Options()
        options.add_experimental_option("detach", True)
        #options.add_argument("--headless")
        ua = UserAgent()
        userAgent = ua.random
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        

    def target_url(self,url):
        self.next_page(url)


    def result_scrap(self,resp):
        data = resp.xpath("//a[@class='absolute bottom-0 left-0 right-0 top-0 z-10 t-c']/@href").getall()
        for dat in data:
            results = str(dat)
            results = f"https://www.goudengids.be{results}"
            with open("links.csv",'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([results])

                
    def next_page(self,url):
        html = requests.get(url).content
        resp = Selector(text=html)
        self.result_scrap(resp)
        
        next_pages_check = resp.xpath("normalize-space(//a[@class='flex h-8 items-center justify-center p-2 rounded-full w-8 cursor-pointer']/@href)").extract_first()
        print("check",next_pages_check)
        if next_pages_check == None:
            None
        else:
            time.sleep(2)
            next_pages_check = str(next_pages_check)
            next_pages_check = f"https://www.goudengids.be{next_pages_check}"
            print("Current_url",next_pages_check)
            self.next_page(next_pages_check)
        
        


    def scrap(self):
         with open("links.csv", 'r') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            for i in reader:
                link = i[0]
                html = requests.get(link).content
                resp = Selector(text=html)
                
                scrap_today = date.today()
                Company_Name = resp.xpath("normalize-space(//h1/text())").extract_first()

                tel_1 = resp.xpath("normalize-space((//span[@itemprop='telephone'])[1]/text())").extract_first()


                tel_2 = resp.xpath("normalize-space((//span[@itemprop='telephone'])[2]/text())").extract_first()
                tel_3 = resp.xpath("normalize-space((//span[@itemprop='telephone'])[3]/text())").extract_first()
                streeet_address = resp.xpath("normalize-space((//span[@data-yext='street']/text())[1])").extract_first()
                city_address = resp.xpath("normalize-space((//span[@data-yext='city']/text())[1])").extract_first()
                city_district_address = resp.xpath("normalize-space((//span[@data-yext='city-district']/text())[1])").extract_first()
                postal_code = resp.xpath("normalize-space((//span[@data-yext='postal-code']/text())[1])").extract_first()
                email = resp.xpath("normalize-space(//a[contains(@href,'mailto:')]/@href)").extract_first()
                email = str(email)
                website = resp.xpath("normalize-space(//span[contains(text(),'Website')]/parent::a/@href)").extract_first()
                website = str(website)
                website = website.replace('?utm_source=fcrmedia&utm_medium=internet&utm_campaign=goudengidspagesdor','')
                website = website.strip()
                reviews = resp.xpath("normalize-space((//meta[@itemprop='ratingValue']/@content)[1])").extract_first()
                no_of_reviews = resp.xpath("normalize-space((//meta[@itemprop='ratingCount']/@content)[1])").extract_first()
                
                e_mail = re.findall(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+',email)
                e_mail = str(e_mail)
                e_mail = e_mail.replace('[','')
                e_mail = e_mail.replace(']','')
                e_mail = e_mail.replace('"','')
                e_mail = e_mail.replace("'","")
                e_mail = e_mail.strip()
                service_catagories = resp.xpath("//a[@class='category']/span/text()").getall()
                desc = resp.xpath("//section[@id='GO__single-activity']//text()").getall()
                desc = str(desc)
                desc = desc.replace("[","")
                desc = desc.replace("]","")
                desc = desc.replace(",","")
                desc = desc.replace("'","")
                desc = desc.replace('"','')
                desc = desc.strip()
                desc = ' '.join(desc.split())
                desc = re.sub(r"\n","",desc)
                desc = str(desc)
                desc = desc.strip()

                print()
                print("trefwoord:",self.keyword)
                print("Bedrijfsnaam:",Company_Name)
                print("telefoon:",tel_1)
                print("telefoon 2:",tel_2)
                print("telefoon 3:",tel_3)
                print("Street_adres:",streeet_address)
                print("city_adres:",city_address)
                print("city_district_adres:",city_district_address)
                print("postal_code:",postal_code)
                print("E-mail:",e_mail)
                print("website:",website)
                print("Beoordelingen van 5:",reviews)
                print("Aantal beoordelingen:",no_of_reviews)
                print("Datumschroot:",scrap_today)
                print("Categorieën Tags:",service_catagories)
                print("Beschrijving:",desc)
                print("link:",link)
                print()
                
                
                with open("Dataset.csv",'a',newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if self.count == 0:
                        writer.writerow(['trefwoord','Bedrijfsnaam','telefoon','telefoon 2','telefoon 3','Street adres','City adres','City District adres','Postal Code','E-mail','website','Beoordelingen van 5','Aantal beoordelingen','Datumschroot','Catagories_tags','Beschrijving','Scraped Link'])
                    writer.writerow([self.keyword,Company_Name,tel_1,tel_2,tel_3,streeet_address,city_address,city_district_address,postal_code,e_mail,website,reviews,no_of_reviews,scrap_today,service_catagories,desc,link])
                    self.count = self.count + 1
                    print("Data saved in CSV: ",self.count)         
                    

if __name__ == '__main__':
    urls = [
        "https://www.goudengids.be/zoeken/vastgoed/East+Flanders/171/",
        # "https://www.goudengids.be/zoeken/immo/East+Flanders/",
        # "https://www.goudengids.be/zoeken/immobili%C3%ABn/East+Flanders/",
        # "https://www.goudengids.be/zoeken/vastgoed+binnenland/East+Flanders/",
        # "https://www.goudengids.be/zoeken/vastgoed+buitenland/East+Flanders/",
    ]
    
    scraper = Serviceseeking()
    # for url in urls:
    #     scraper.target_url(url)
    scraper.scrap()
