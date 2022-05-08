from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    page_count = 0
    count = 0
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
        #
        username = 'gokmen@appsamurai.com'
        password = '128815Gk!'
        search = self.driver.find_element(By.XPATH, "//input[@type='email' and @placeholder='Email']")
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        time.sleep(1)
        search.send_keys(username)
        time.sleep(1)

        search1 = self.driver.find_element(By.XPATH, "//input[@type='password']")
        search1.send_keys(Keys.CONTROL + "a")
        search1.send_keys(Keys.DELETE)
        time.sleep(1)
        search1.send_keys(password)
        time.sleep(3)

        self.driver.find_element(By.XPATH, "//button[contains(text(),'Log in to My MWC')]").click()
        time.sleep(20)
        

        #//h3[@id='session_timeout-title']/@id

    
    def target_url(self,url):
        self.driver.get(url)
        time.sleep(10)
        try:
            self.driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']").click()
            time.sleep(5)
        except:
            None

    def catagory_select(self):
        self.driver.find_element(By.XPATH, "//option[contains(text(),'App/Software Development')]").click()
        time.sleep(5)
        
    def back(self):
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(5)
                
    def next_button(self):
        time.sleep(4)
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Next')]")))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(5)
    
    def next_page(self):
        for i in range(0,self.page_count):
            self.next_button()
        self.result_scrap()
        self.next_page()

    def result_scrap(self):
        time.sleep(5)
        data = self.driver.find_elements(By.XPATH, "//div[@class='flex flex-row justify-between content-center p-4 hover:bg-gray-100 cursor-pointer mr-4']")
        for da in range(0,len(data)):
            element = self.driver.find_elements(By.XPATH, "//div[@class='flex flex-row justify-between content-center p-4 hover:bg-gray-100 cursor-pointer mr-4']")[da]
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
            self.scrap()
            self.back()
            for i in range(0,self.page_count):
                self.catagory_select()
                self.next_button()
            self.catagory_select()
        self.page_count = self.page_count + 1


    def scrap(self):
        html = self.driver.page_source
        resp = Selector(text=html)
        
        
        name = resp.xpath("//span[@class='text-4xl flex flex-row align-center']/text()").getall()
        name = str(name)
        name = name.replace('[','')
        name = name.replace(']','')
        name = name.replace('"','')
        name = name.replace("'","")
        name = name.replace(",","")
        name = name.strip()
        job_function = resp.xpath("normalize-space(//div[contains(text(),'Job Function')]/following-sibling::div[1]/text())").extract_first()
        area_of_responsibilities = resp.xpath("normalize-space(//div[contains(text(),'Area of Responsibility')]/following-sibling::div[1]/text())").extract_first()
        company_main_activity = resp.xpath('''normalize-space(//div[contains(text(),"Company's Main Activity")]/following-sibling::div[1]/text())''').extract_first()
        role = resp.xpath("normalize-space(//div[@class='mt-4 text-xl font-semibold']/text())").extract_first()
        company = resp.xpath("normalize-space(//div[@class='mt-4 text-xl font-semibold']/following-sibling::div[1]/text())").extract_first()
        city = resp.xpath("normalize-space(//div[@class='mt-4 text-xl font-semibold']/following-sibling::p[1]/text())").extract_first()
        location = resp.xpath("normalize-space(//div[@class='mt-4 text-xl font-semibold']/following-sibling::p/span/text()[last()])").extract_first()
        interest_Tags = resp.xpath("//div[contains(text(),'Interest Tags')]/following-sibling::div/span/text()").getall()
        skills = resp.xpath("//div[contains(text(),'Skills ')]/following-sibling::div/span/text()").getall()
        
        print()
        print("name:",name) #A
        print("job_function:",job_function) #B
        print("area_of_responsibilities:",area_of_responsibilities) #C
        print("company_main_activity:",company_main_activity) #D
        print("role:",role) #D
        print("company:",company) #D
        print("city:",city) #D
        print("location:",location) #D
        print("interest_Tags:",interest_Tags) #D
        print("skills:",skills) #D
        print("Scraped Links",self.driver.current_url)
        print()
        
        with open("Dataset.csv",'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            if self.count == 0:
                writer.writerow(['name','job_function','location','area_of_responsibilities','company_main_activity','role','company','city','location','interest_Tags','skills','Scraping Links'])
            writer.writerow([name,job_function,location,area_of_responsibilities,company_main_activity,role,company,city,location,interest_Tags,skills,self.driver.current_url])
            self.count = self.count + 1
            print("Data saved in CSV: ",self.count)
                    

if __name__ == '__main__':
    url = "https://www.mwcbarcelona.com/mymwc"
    url_1 = "https://www.mwcbarcelona.com/attendees"
    
    scraper = Serviceseeking()
    scraper.start()
    scraper.target_url(url)
    scraper.login()
    scraper.target_url(url_1)
    scraper.catagory_select()
    scraper.next_page()
