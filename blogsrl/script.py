from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
    def __init__(self):
        try:
            self.df = pd.read_excel(self.path)
        except:
            self.df = pd.DataFrame({
                'Barcode': [], 
                'Price per Item': [],
                'Price per Cart':[],
                'Scraped Link':[]
            })
        
    def start(self):
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
    
    def login(self):
        self.driver.get("https://blogsrl.it/gb/login")
        time.sleep(5)
        try:
            element = self.driver.find_element_by_xpath("//button[@id='cookieModalConsent']")
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
        except:
            None


        search = self.driver.find_element_by_xpath("//input[@name='email' and @class='form-control']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys("office@yollo.eu")
        time.sleep(1)

        search1 = self.driver.find_element_by_xpath("//input[@name='password']")
        search1.send_keys(Keys.CONTROL + "a")
        search1.send_keys(Keys.DELETE)
        time.sleep(1)
        search1.send_keys("project2022")
        time.sleep(1)

        self.driver.find_element_by_xpath("//button[contains(text(),'Sign i')]").click()
        time.sleep(30)
        

    
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
            
            self.scrap(results)


    def scrap(self):
        with open("links.csv", 'r',encoding='utf-8') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            for i in reader:
                link = str(i[0])
                self.driver.get(link)
                time.sleep(4)
                html = self.driver.page_source
                resp = Selector(text=html)
                check = resp.xpath("normalize-space(//h1[contains(text(),'502 Bad Gateway')])").extract_first()
                if check:
                    self.driver.close()
                    self.start()
                    self.login()
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
    scraper.start()
    scraper.login()
    scraper.scrap()
    # for url in urls:
    #     scraper.target_url(url)
