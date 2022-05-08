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

count = 0
ul = "https://opencorporates.com/companies/us_fl"
path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get(ul)
time.sleep(2)
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name","Incorporation_Date","Company_type","Jurisdiction","Agent_name","Agent_address","Director_office","Head_address","Mail_address","Identifier_system","Identifier"])
def scrap_data(html):
    name = resp.xpath("normalize-space(//h1[@class='wrapping_heading fn org']/text())").extract_first()
    Incorporation_Date = resp.xpath("//span[@itemprop='foundingDate']/text()").extract_first()
    company_type = resp.xpath("//dd[@class='company_type']/text()").extract_first()
    Jurisdiction = resp.xpath("//dd[@class='jurisdiction']/a/text()").extract_first()
    agent_name = resp.xpath("//dd[@class='agent_name']/text()").extract_first()
    agent_address = resp.xpath("//dd[@class='agent_address']/text()").extract_first()
    director_office = resp.xpath("//dd[@class='officers trunc8']//text()").getall()
    head_address = resp.xpath("normalize-space((//p[@class='description']/text())[1])").get()
    mail_address = resp.xpath("normalize-space((//p[@class='description']/text())[2])").get()
    identifier_system = resp.xpath("(//table[@class='table table-condensed table-striped company-data-object']/tbody/tr/td)[1]/text()").get()
    identifier = resp.xpath("(//table[@class='table table-condensed table-striped company-data-object']/tbody/tr/td)[2]/text()").get()
    with open('test.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name,Incorporation_Date,company_type,Jurisdiction,agent_name,agent_address,director_office,head_address,mail_address,identifier_system,identifier])
        print("Data Saved in CSV")
with open("./input.csv", 'r') as input_file:
    for code in input_file:
        company = code.strip()
        search = driver.find_element_by_xpath("//input[@id='q']")
        time.sleep(1)
        search.clear()
        search.send_keys(company)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            soup = driver.page_source
            resp = Selector(text=soup)
            active_links = resp.xpath("//a[@class='company_search_result active']/@href").getall()
            inactive_links = resp.xpath("//ul[@id='companies']/li//a[@class='company_search_result inactive inactive']/@href").getall()
            try:
                for link in active_links:
                    a = f"https://opencorporates.com{link}"
                    driver.get(a)
                    time.sleep(2)
                    soup = driver.page_source
                    resp = Selector(text=soup)
                    scrap_data(resp)
                    
            except:
                print("No active link is found.")
            try:
                for link in inactive_links:
                    b = f"https://opencorporates.com{link}"
                    driver.get(b)
                    time.sleep(2)
                    soup = driver.page_source
                    resp = Selector(text=soup)
                    name = resp.xpath("//h1[@class='wrapping_heading fn org']/text()").extract_first()
                    scrap_data(resp)
            except:
                print("No active link is found.")
            driver.get(ul)
            time.sleep(2)
        except:
            print("Search Result is empty")
            driver.get(ul)
            time.sleep(3)

driver.close()
        