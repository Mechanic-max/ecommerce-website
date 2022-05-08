from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
import time
from scrapy.selector import Selector
import csv
import re
class Solicitors():

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
        

    def target_url(self):
        with open("links.csv", 'r',encoding='utf-8') as input_file:
            reader = csv.reader(input_file,delimiter=",")
            for i in reader:
                link = str(i[0])
            try:
                self.driver.get(link)
            except:
                self.driver.close()
                self.start()
                self.driver.get(link)

            time.sleep(5)
            self.next_page()
        
    def result_scrap(self):
        total_result = self.driver.find_elements_by_xpath("//h2/a")
        for i in range(0,len(total_result)):
            self.driver.find_elements_by_xpath("//h2/a")[i].click()
            time.sleep(3)
            self.scrap()
            self.driver.execute_script("window.history.go(-1)")
            time.sleep(3)
    
    
    def next_page(self):
        html = self.driver.page_source
        resp = Selector(text=html)
        self.result_scrap()
        next_page_check = resp.xpath("(//a[contains(text(),'Next')]/text())[1]").extract_first()
        print(next_page_check)
        if next_page_check == None:
            None
        elif next_page_check:
            self.driver.find_elements_by_xpath("//a[contains(text(),'Next')]")[0].click()
            time.sleep(4)
            self.next_page()
        



    def scrap(self):
        html = self.driver.page_source
        resp = Selector(text=html)
        company_name = resp.xpath("normalize-space(//h1/text())").extract_first()
        associate = ""
        head_office_address = resp.xpath("//dt[contains(text(),'Address:')]/following-sibling::dd[1]/text()").getall()
        if head_office_address == []:
            head_office_address = resp.xpath("//dt[contains(text(),'Tel')]/parent::dl/following-sibling::dl/dt/following-sibling::dd[1]/text()").getall()
            associate  = resp.xpath("//dt[contains(text(),'Tel')]/parent::dl/following-sibling::dl/dt/following-sibling::dd[1]/a[contains(@href,'/office')]/text()").extract_first()
        date = resp.xpath("normalize-space(//h1/following-sibling::p/span/text())").extract_first()
        head_office_address = str(head_office_address)
        head_office_address = head_office_address.replace("[","")
        head_office_address = head_office_address.replace("]","")
        head_office_address = head_office_address.replace(",","")
        head_office_address = head_office_address.replace("'","")
        head_office_address = head_office_address.replace('"','')
        head_office_address = head_office_address.strip()
        head_office_address = ' '.join(head_office_address.split())
        head_office_address = str(head_office_address)
        head_office_address = re.sub("\Wn+","",head_office_address)
        head_office_address = head_office_address.strip()
        tel = resp.xpath("normalize-space(//dt[contains(text(),'Tel:')]/following-sibling::dd[1]/text())").extract_first()
        tel = str(tel)
        if tel:
            tel = f"Ph {tel}"
        url = self.driver.current_url
        type = resp.xpath("normalize-space(//dt[contains(text(),'Type:')]/following-sibling::dd[1]/text())").extract_first()
        sra_id = resp.xpath("normalize-space(//dt[contains(text(),'SRA ID:')]/following-sibling::dd[1]/text())").extract_first()
        sra_regulated = resp.xpath("normalize-space(//em[contains(text(),'SRA Regulated')]/text())").extract_first()
        sra_regulated = str(sra_regulated)
        sra_regulated_check = False
        if sra_regulated == 'SRA Regulated':
            sra_regulated_check = True
        email = resp.xpath("normalize-space(//dt[contains(text(),'Email:')]/following-sibling::dd[1]/a/text())").extract_first()
        web = resp.xpath("normalize-space(//dt[contains(text(),'Web:')]/following-sibling::dd[1]/a/text())").extract_first()
        areas_of_practice_at_this_bracnh = resp.xpath("//div[@id='branch-areas-of-practice-accordion']/ul/li//text()").getall()
        areas_of_practice_at_this_bracnh = str(areas_of_practice_at_this_bracnh)
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.replace("[","")
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.replace("]","")
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.replace(",","")
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.replace("'","")
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.replace('"','')
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.strip()
        areas_of_practice_at_this_bracnh = ' '.join(areas_of_practice_at_this_bracnh.split())
        areas_of_practice_at_this_bracnh = str(areas_of_practice_at_this_bracnh)
        areas_of_practice_at_this_bracnh = re.sub("\Wn+","",areas_of_practice_at_this_bracnh)
        areas_of_practice_at_this_bracnh = areas_of_practice_at_this_bracnh.strip()

        areas_of_practise_at_this_organisation = resp.xpath("//div[@id='areas-of-practice-accordion']/ul/li//text()").getall()
        areas_of_practise_at_this_organisation = str(areas_of_practise_at_this_organisation)
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.replace("[","")
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.replace("]","")
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.replace(",","")
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.replace("'","")
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.replace('"','')
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.strip()
        areas_of_practise_at_this_organisation = ' '.join(areas_of_practise_at_this_organisation.split())
        areas_of_practise_at_this_organisation = str(areas_of_practise_at_this_organisation)
        areas_of_practise_at_this_organisation = re.sub("\Wn+","",areas_of_practise_at_this_organisation)
        areas_of_practise_at_this_organisation = areas_of_practise_at_this_organisation.strip()

        self.print_save(company_name,head_office_address,tel,url,sra_id,sra_regulated_check,type,email,web,areas_of_practice_at_this_bracnh,areas_of_practise_at_this_organisation,associate,date)  
            
            


    def print_save(self,company_name,head_office_address,tel,url,sra_id,sra_regulated_check,type,email,web,areas_of_practice_at_this_bracnh,areas_of_practise_at_this_organisation,associate,date):
        print()
        print("company_name:",company_name)
        print("head_office_address:",head_office_address)
        print("tel:",tel)
        print("url:",url)
        print("sra_id:",sra_id)
        print("sra_regulated_check:",sra_regulated_check)
        print("type:",type)
        print("email:",email)
        print("web:",web)
        print("areas_of_practice_at_this_bracnh:",areas_of_practice_at_this_bracnh)
        print("areas_of_practise_at_this_organisation:",areas_of_practise_at_this_organisation)
        print("associate:",associate)
        print("date:",date)
        print()
        with open("Dataset.csv",'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            if self.count == 0:
                writer.writerow(['Company Name','Head Office Address','Tel','Link','Type','SRA ID','SRA Regulated','Email','Web','Areas od practice at this bracnh','areas of practise at this organisation','associate','date'])
            writer.writerow([company_name,head_office_address,tel,url,type,sra_id,sra_regulated_check,email,web,areas_of_practice_at_this_bracnh,areas_of_practise_at_this_organisation,associate,date])
            self.count = self.count + 1
            print("Data saved in CSV: ",self.count)  

    def close(self):
        self.driver.close()
if __name__ == '__main__':
    scraper = Solicitors()
    scraper.start()
    scraper.target_url()
    scraper.close()