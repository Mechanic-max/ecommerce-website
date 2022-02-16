from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
import chromedriver_binary
from fake_useragent import UserAgent
import time
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime
import requests
from requests.structures import CaseInsensitiveDict
import sys
class kijihi():

    """
    proxies = [
        ""
        ]
    
    """
    count = 0
    links =[]
    

    def start(self):
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        options.add_argument(f'user-agent={ua}')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://google.com')
        time.sleep(2)
    


    def target_url(self,url):
        self.driver.get(url)
        time.sleep(60)
        self.next_page()

    def result_scrap(self):
        html = self.driver.page_source
        resp = Selector(text=html)
        results = resp.xpath("//div[contains(@class,'ProductTile')]")
        for ri in results:
            li = ri.xpath(".//div/h3[@class='product-brand-name']/a/@href").extract_first()
            li = str(li)
            li = li.strip()
            li = f"https://www.liquorland.com.au{li}"
            self.links.append(li)

   
    
    def next_page(self):
        try:
            self.result_scrap()
            next_button = self.driver.find_element_by_xpath("//button[contains(@title,'next')]")
            if next_button:
                next_button.click()
                time.sleep(20)
                self.next_page()
        except:
            None
            

    def header(self,out_name):
        with open(out_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["scrape_date","website_url","Product_ID","GTIN","Brand","product","price","pack_size","multibuy_deal_quantity","multibuy_deal_price","undiscounted_price","delivery_available","review_rating","review_count","style","type","packaging","standard_drinks","alcohol_content","organic","origin"])


    def scrap(self,scrape_date,out_name):
        self.header(out_name)
        for ulo in self.links:
            self.driver.get(ulo)
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(),'Product ID')]/following-sibling::span")))
            except:
                None

            time.sleep(7)
            html = self.driver.page_source
            resp = Selector(text=html)

            website_url = str(ulo)
            Product_ID = resp.xpath("normalize-space(//span[contains(text(),'Product ID')]/following-sibling::span/text())").extract_first()
            GTIN = resp.xpath("normalize-space(//span[contains(text(),'GTIN')]/following-sibling::span/text())").extract_first()

            Brand = resp.xpath("//span[contains(text(),'Brand')]/following-sibling::span/a/text()").extract_first()
            product = resp.xpath("(//div[@class='product-name'])[1]/text()").extract_first()
            price = resp.xpath("normalize-space((//span[@class='PriceTag zero-cents current primary']//span[@class='dollarAmount'])[1]/text())").extract_first()

            pack_size = resp.xpath("normalize-space((//span[@class='unitOfMeasure'])[1]/text())").extract_first()

            multibuy_deal_quantity = resp.xpath("normalize-space(//div[@class='callout callout-text' and contains(text(),' for ')]/text())").extract_first()
            multibuy_deal_quantity = str(multibuy_deal_quantity)
            m_deal_quantity = re.findall(r"^([\w\-]+)",multibuy_deal_quantity)
            m_deal_quantity = str(m_deal_quantity)
            m_deal_quantity = m_deal_quantity.replace("'","")
            m_deal_quantity = m_deal_quantity.replace("[","")
            m_deal_quantity = m_deal_quantity.replace("]","")
            m_deal_quantity = m_deal_quantity.strip()

            multibuy_deal_quantity = multibuy_deal_quantity.replace(m_deal_quantity,'')
            multibuy_deal_quantity = multibuy_deal_quantity.replace('for','')
            multibuy_deal_quantity = multibuy_deal_quantity.replace('$','')
            multibuy_deal_price = multibuy_deal_quantity.strip()

            undiscounted_price = resp.xpath("(//span[contains(text(),'Price reduced from')])[1]/following-sibling::div/span[@class='dollarAmount']/text()").extract_first()
            
            delivery_available = resp.xpath("(//span[contains(text(),'Delivery')])[last()-3]/text()").extract_first()
            if delivery_available == "Delivery":
                delivery_available = True
            else:
                delivery_available = False

            review_rating = resp.xpath("//div[contains(@class,'bv_avgRating_component_container')]/text()").extract_first()
            review_count = resp.xpath("//div[contains(@class,'bv_numReviews_text')]/text()").extract_first()
            review_count = str(review_count)
            review_count = review_count.replace('-','')
            review_count = review_count.replace('(','')
            review_count = review_count.replace(')','')
            review_count = review_count.strip()
            style = resp.xpath("//span[contains(text(),'Style')]/following-sibling::span/text()").extract_first()
            type = resp.xpath("//span[contains(text(),'Type')]/following-sibling::span/text()").extract_first()
            packaging = resp.xpath("//span[contains(text(),'Packaging')]/following-sibling::span/text()").extract_first()
            standard_drinks = resp.xpath("//span[contains(text(),'Standard Drinks')]/following-sibling::span/text()").extract_first()
            alcohol_content = resp.xpath("//span[contains(text(),'Alcohol Content')]/following-sibling::span/text()").extract_first()
            organic = resp.xpath("//span[contains(text(),'Organic')]/following-sibling::span/text()").extract_first()
            origin = resp.xpath("//span[contains(text(),'Origin')]/following-sibling::span/text()").extract_first()


            print()
            print("scrape_date",scrape_date)
            print("website_url:",website_url)
            print("Product_ID:",Product_ID)
            print("GTIN:",GTIN)
            print("Brand:",Brand)
            print("product:",product)
            print("price:",price)
            print("pack_size:",pack_size)
            print("multibuy_deal_quantity:",m_deal_quantity)
            print("multibuy_deal_price:",multibuy_deal_price)
            print("undiscounted_price:",undiscounted_price)
            print("delivery_available:",delivery_available)
            print("review_rating:",review_rating)
            print("review_count:",review_count)
            print("style:",style)
            print("type:",type)
            print("packaging:",packaging)
            print("standard_drinks:",standard_drinks)
            print("alcohol_content:",alcohol_content)
            print("organic:",organic)
            print("origin:",origin)
            print()

            
            
            with open(out_name,'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([scrape_date,website_url,Product_ID,GTIN,Brand,product,price,pack_size,m_deal_quantity,multibuy_deal_price,undiscounted_price,delivery_available,review_rating,review_count,style,type,packaging,standard_drinks,alcohol_content,organic,origin])
                self.count = self.count + 1
                print("Data saved in excel: ",self.count)

    def close(self):
        self.driver.close()



if __name__ == '__main__':
    
    out_name = sys.argv[1]
    scrape_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    scraper = kijihi()
    scraper.start()
    url = "https://www.liquorland.com.au/beer"

    scraper.target_url(url)
    scraper.scrap(scrape_date,out_name)
    scraper.close()