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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv
from selenium.webdriver.support.ui import Select
import re
import datetime

class Serviceseeking():
    count = 0
    keyword = ''
    def __init__(self):
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless")
        # # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')

        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options,desired_capabilities=capa)
        

    def target_url(self,url):
        self.driver.get(url)
        time.sleep(5)
        self.next_page()


    def result_scrap(self):
        html = self.driver.page_source
        resp = Selector(text=html)
        self.keyword = resp.xpath("normalize-space(//span[@itemprop='name']/text())").extract_first()
        data = resp.xpath("//div[contains(@class,'visible')]/a[contains(@href,'/profile')]")
        for dat in data:
            results = dat.xpath("..//@href").extract_first()
            address_city = dat.xpath("..//div[@class='font-14 text-gray suburb-name']/text()").extract_first()
            results = str(results)
            results = f"https://www.serviceseeking.com.au{results}"
            with open("links.csv",'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([results,address_city,self.keyword])

                
    def next_page(self):
        while True:
            try:
                self.driver.find_element_by_xpath("//button[contains(text(),'View More')]").click()
                time.sleep(5)
            except:
                break
        time.sleep(2)
        self.result_scrap()


    def scrap(self):
         with open("links.csv", 'r') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            for i in reader:
                link = i[0]
                city_address = i[1]
                self.keyword = i[2]
                try:
                    self.driver.get(link)
                    time.sleep(15)
                    self.driver.set_page_load_timeout(15)
                except:
                    self.driver.execute_script("window.stop();")
                


                
                html = self.driver.page_source
                resp = Selector(text=html)
                
                
                business_name = resp.xpath("normalize-space(//div[@itemprop='name']/text())").extract_first()
                

                persons_name = resp.xpath("normalize-space((//div[@class='text-copy-2 font-14'])[1]/text())").extract_first()


                address = resp.xpath("normalize-space((//div[@class='text-copy-2 font-14'])[2]/text())").extract_first()
                abn_no = resp.xpath("normalize-space(//strong[contains(text(),'ABN -')]/parent::div/text())").extract_first()

                ph_no1 = ''
                ph_no2 = ''
                fax_no = ''

                try:
                    self.driver.find_element_by_xpath("//a[contains(@class,'btn btn-block btn-md btn-blue-extra-light radius-10 text-left')]").click()
                    time.sleep(5)
                except:
                    None
                
                html = self.driver.page_source
                resp = Selector(text=html)

                ph_no1 = resp.xpath("normalize-space(//a[contains(@href,'tel')]/span/text())").extract_first()
                
                email = ''
                service_catagories = resp.xpath("//h3[contains(text(),'SERVICES WE PROVIDE')]/parent::div/following-sibling::div//div[@class='panel']//div[@class='panel-body']/div//text()").getall()
                
                print()
                print("keyword:",self.keyword)
                print("persons_name:",persons_name)
                print("business_name:",business_name)
                print("address:",address)
                print("city_address:",city_address)
                print("abn_no:",abn_no)
                print("ph_no1:",ph_no1)
                print("ph_no2:",ph_no2)
                print("fax_no:",fax_no)
                print("email:",email)
                print("service_catagories:",service_catagories)
                print("link:",link)
                print()
                
                
                with open("Dataset_Serviceseeking.csv",'a',newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if self.count == 0:
                        writer.writerow(['Keyword','Persons Name','Business Name','Street Address','City','ABN NO','Contact Number 1','Contact Number 2','Fax No','Email','Service Catagories','link'])
                    writer.writerow([self.keyword,persons_name,business_name,address,city_address,abn_no,ph_no1,ph_no2,fax_no,email,service_catagories,link])
                    self.count = self.count + 1
                    print("Data saved in CSV: ",self.count)         
                    

if __name__ == '__main__':
    urls = [
        "https://www.serviceseeking.com.au/coloured-concrete",
        "https://www.serviceseeking.com.au/concrete-cladding",
        "https://www.serviceseeking.com.au/concrete-cleaning",
        "https://www.serviceseeking.com.au/concrete-core-drilling",
        "https://www.serviceseeking.com.au/concrete-cutting",
        "https://www.serviceseeking.com.au/concrete-driveway",
        "https://www.serviceseeking.com.au/concrete-driveways-and-paths",
        "https://www.serviceseeking.com.au/concrete-edging",
        "https://www.serviceseeking.com.au/concrete-fencing",
        "https://www.serviceseeking.com.au/concrete-footpaths",
        "https://www.serviceseeking.com.au/concrete-formwork",
        "https://www.serviceseeking.com.au/concrete-foundations",
        "https://www.serviceseeking.com.au/concrete-painting",
        "https://www.serviceseeking.com.au/concrete-pavers",
        "https://www.serviceseeking.com.au/concrete-polishing",
        "https://www.serviceseeking.com.au/concrete-pumping",
        "https://www.serviceseeking.com.au/concrete-removal",
        "https://www.serviceseeking.com.au/concrete-repair",
        "https://www.serviceseeking.com.au/concrete-resurfacing",
        "https://www.serviceseeking.com.au/concrete-retaining-walls",
        "https://www.serviceseeking.com.au/concrete-slab",
        "https://www.serviceseeking.com.au/concreters",
        "https://www.serviceseeking.com.au/exposed-aggregate-concrete",
    ]
    
    scraper = Serviceseeking()
    # for url in urls:
    #     scraper.target_url(url)
    scraper.scrap()
