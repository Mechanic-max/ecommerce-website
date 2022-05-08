from selenium import webdriver
import scrapy
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv
from pandas import DataFrame

path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get("https://www.fashiontiy.com/men-swimwear.html")
time.sleep(2)

def aloo():
    color,siz,images,qity_pri=[],[],[],[]
    try:
        coli_item = driver.find_elements_by_xpath("//div[@class='color_colors']/div")
        for i in range(0,len(coli_item)):
            btn = driver.find_elements_by_xpath("//div[@class='color_colors']/div")[i]
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
            col = driver.find_element_by_xpath("//div[@class='base_key_value size_title_left']/span[@class='notranslate']").text
            color.append(col)
            img = driver.find_elements_by_xpath("//div[@class='detail_left']/div[@class='left_thums']/img")
            for im in range(0,len(img)):
                img = driver.find_elements_by_xpath("//div[@class='detail_left']/div[@class='left_thums']/img")[im].get_attribute("src")
                images.append(img)
                
            sizes = driver.find_elements_by_xpath("//div[@class='size_list notranslate']/div/span[@class='size_item_name ']")
            for j in range(0,len(sizes)):
                sizes_avaiable = driver.find_elements_by_xpath("//div[@class='size_list notranslate']/div/span[@class='size_item_name ']")[j].text
                siz.append(sizes_avaiable)
        
        g1 =  ', '.join(images)
        g2 =  '|'.join(siz) 
        g3 = ', '.join(color)
    except:
        print("There is nothing to scrape.")

    html = driver.page_source 
    resp = Selector(text=html)
    for xlo in resp.xpath("//div[@class='right_price_parent']/div"):
        Quantity_price = xlo.xpath(".//p/text()").getall()
        qity_pri.append(Quantity_price)

    absolute_id = ""
    Id = resp.xpath("//div[@class='right_title notranslate']/text()").get()
    absolute_id = Id
    absolute_id = absolute_id.replace("SKU:","")
    absolute_id = absolute_id.lstrip()
    Name = resp.xpath("//div[@class='right_desc']/span/text()").get()
    Min_order_req = resp.xpath("//div[@class='right_moq base_key_value']/span[@class='notranslate']/text()").get()
    Gross_Weight = resp.xpath("(//div[@class='base_key_value']/span[not(contains(@class,'key'))])[1]/text()").get()
    Material = resp.xpath("(//div[@class='base_key_value']/span[not(contains(@class,'key'))])[2]/text()").get()
        
    with open("mens_swimwear.csv", 'a',newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([absolute_id,Name,Min_order_req,g3,qity_pri,g2,g1,Gross_Weight,Material])
        print("Data Saved in CSV :")
def moli():

    links = driver.find_elements_by_xpath("//div[@class='list_products']/div//a[@class='product_infos_2 notranslate']")
    for i in range(0,len(links)):
        link = driver.find_elements_by_xpath("//div[@class='list_products']/div//a[@class='product_infos_2 notranslate']")[i].get_attribute("href")
        driver.get(link)
        time.sleep(2)
        aloo()

        driver.back()
        time.sleep(5)
    next_page = driver.find_element_by_xpath("//div[contains(text(),'NEXT')]")
    if next_page:
        next_page.click()
        time.sleep(4)
        moli()



with open("mens_swimwear.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID","Name","Minimum Order requirenment","color","Quantity and price","Size","images_url","Gross Weight","Material"])
moli()