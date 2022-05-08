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

class Porch():
    count = 0
    links = []
    keyword = 'drain-cleaning'
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
        self.driver.get(url)
        time.sleep(25)
        self.get_page_links()

    def get_page_links(self):
        html = self.driver.page_source
        resp = Selector(text=html)

        all_cities_links = resp.xpath("//a[@class='topCities-row-link']/@href").getall()
        for acl in all_cities_links:
            acl = str(acl)
            acl = acl.strip()
            acl = f"https://porch.com{acl}"
            self.driver.get(acl)
            time.sleep(15)
            self.result_scrap()

    def result_scrap(self):
        time.sleep(1)
        html = self.driver.page_source
        resp = Selector(text=html)
        self.keyword = resp.xpath("normalize-space((//span[@itemprop='name'])[2]/text())").extract_first()
        data = resp.xpath("//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-6 MuiGrid-item MuiGrid-grid-xs-12']//div[@class='MuiGrid-root jss3 jss4 MuiGrid-item']")
        for dat in data:
            results = dat.xpath("normalize-space(..//h3/a/@href)").extract_first()
            with open("links.csv",'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([results])
        
    def close(self):
        self.driver.close()
    
    def scrap(self):
        with open("links.csv", 'r') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            for i in reader:
                link = i[0]
        # for link in self.links:
                self.driver.get(link)
                time.sleep(2)
                html = self.driver.page_source
                resp = Selector(text=html)

                check = resp.xpath("//span[contains(text(),'Click to verify')]/text()").extract_first()
                print("Check",check)
                if check:
                    try:
                        self.driver.find_element_by_xpath("//span[contains(text(),'Click to verify')]/parent::div").click()
                        time.sleep(3)
                    except:
                        print("idhr bi asy hi")
                    self.close()
                    self.start()
                    self.driver.get(link)
                    time.sleep(30)
                    html = self.driver.page_source
                    resp = Selector(text=html)
                
                
                business_name = resp.xpath("normalize-space(//h1[@class='heading-companyName']/text())").extract_first()
                

                persons_name = resp.xpath("normalize-space((//a[@class='no-style'])[1]/text())").extract_first()

                address = resp.xpath("normalize-space(//div[@class='address']/text())").extract_first()
                
                city_address = resp.xpath("normalize-space(//div[@class='address']/div/text())").extract_first()


                ph_no1 = ''
                ph_no2 = ''
                fax_no = ''

                try:
                    self.driver.find_element_by_xpath("//a[contains(text(),'Click to view')]").click()
                    time.sleep(5)
                except:
                    None
                
                try:
                    self.driver.find_element_by_xpath("//h4[contains(text(),'Services offered')]/following-sibling::div//a[contains(text(),'Show more')]").click()
                    time.sleep(1)
                except:
                    None
                html = self.driver.page_source
                resp = Selector(text=html)

                ph_no1 = resp.xpath("normalize-space((//div[@class='phone-number-area']/span)[1]/text())").extract_first()
                if ph_no1:
                    None
                else:
                    ph_no1 = resp.xpath("normalize-space(//a[@class='pro-phone-number']/text())").extract_first()
                email = ''
                
                service_catagories = resp.xpath("//h4[contains(text(),'Services offered')]/following-sibling::div/div[@class='services']/div/span/text()").getall()


                print()
                print("keyword:",self.keyword)
                print("persons_name:",persons_name)
                print("business_name:",business_name)
                print("address:",address)
                print("city_address:",city_address)
                print("ph_no1:",ph_no1)
                print("ph_no2:",ph_no2)
                print("fax_no:",fax_no)
                print("email:",email)
                print("service_catagories:",service_catagories)
                print("link:",link)
                print()
                
                
                with open("Dataset_Porch.csv",'a',newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if self.count == 0:
                        writer.writerow(['Keyword','Persons Name','Business Name','Street Address','City','Contact Number 1','Contact Number 2','Fax No','Email','Service Catagories','link'])
                    writer.writerow([self.keyword,persons_name,business_name,address,city_address,ph_no1,ph_no2,fax_no,email,service_catagories,link])
                    self.count = self.count + 1
                    print("Data saved in CSV: ",self.count)         
                    

if __name__ == '__main__':
    urls = ["https://porch.com/near-me/drain-cleaning"]
    
    scraper = Porch()

    scraper.start()
    # for url in urls:
    #     scraper.target_url(url)
    
    scraper.scrap()



# 
# https://porch.com/near-me/drain-cleaning