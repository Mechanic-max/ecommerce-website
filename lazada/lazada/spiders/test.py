import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.action_chains import ActionChains

class TestSpider(scrapy.Spider):
    name = 'test'
    #allowed_domains = ['www.lazada.com.my']
    start_urls = ['https://www.lazada.com.my/shop-software/?spm=a2o4k.pdp_revamp.breadcrumb.3.54b05c1aRaQ9f5']

    def parse(self, response):
        path = which("chromedriver")
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        ua = UserAgent()
        userAgent = ua.random
        chrome_options.add_argument(f'user-agent={userAgent}')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
        driver.get(response.url)
        time.sleep(3)
        n=0
        while True:
            if n == 0:
                try:
                    btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a")
                    if btn_info_page:
                        for wsa in range(0,len(btn_info_page)):
                            btn_info_page = driver.find_elements_by_xpath("//div[@class='c16H9d']/a")[wsa]

                            link = btn_info_page.get_attribute("href")
                            try:
                                image_url_link = driver.find_elements_by_xpath("//img[@class='c1ZEkM ']")[wsa]
                                img = image_url_link.get_attribute("src")
                            except:
                                img = None
                    
                            driver.execute_script("arguments[0].click();", btn_info_page)
                            time.sleep(1)

                            title = driver.find_element_by_xpath("//h1[@class='pdp-mod-product-badge-title']").text
                            regular_price = driver.find_element_by_xpath("//span[@class=' pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl']").text
                            Product_Type = driver.find_element_by_xpath("(//a[@class='breadcrumb_item_anchor']/span)[3]").text
                            content = driver.find_element_by_xpath("//meta[@name='description']").get_attribute("content")
                            try:
                                dropship_supplier = driver.find_element_by_xpath("//a[@class='pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name']").get_attribute("href")
                            except:
                                dropship_supplier = None
                            try:
                                No_of_rating = driver.find_element_by_xpath("//a[@class='pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link']").text
                            except:
                                No_of_rating = None
                            try:
                                precentage_off = driver.find_element_by_xpath("//span[@class='pdp-product-price__discount']").text
                            except:
                                precentage_off = None  
                            try:
                                dis = driver.find_element_by_xpath("//span[@class=' pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs']").text
                            except:
                                dis = None
                            try:
                                stock = driver.find_element_by_xpath("//span[@class='quantity-content-default']").text
                            except:
                                stock = None
                            try:
                                driver.execute_script("window.scrollTo(0, 900)")
                                time.sleep(3)
                                Brand = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[1]").text
                                SKU = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[2]").text
                                model = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[3]").text
                                Receiving_item = driver.find_element_by_xpath("(//div[@class='html-content box-content-html'])").text
                            except:
                                try:
                                    try:
                                        driver.find_element_by_xpath("//button[@class='pdp-view-more-btn pdp-button pdp-button_type_text pdp-button_theme_white pdp-button_size_m']")
                                    except:
                                        driver.execute_script("window.scrollTo(900, 1100)")
                                        time.sleep(2)
                                    
                                    view_more = driver.find_element_by_xpath("//button[@class='pdp-view-more-btn pdp-button pdp-button_type_text pdp-button_theme_white pdp-button_size_m']")
                                    view_more.click()
                                    time.sleep(2)
                                    
                                    try:
                                        driver.execute_script("window.scrollTo(1100, 1600)")
                                        time.sleep(2)
                                        driver.find_element_by_xpath("(//div[@class='html-content box-content-html'])")
                                    except:
                                        driver.execute_script("window.scrollTo(1600, 2000)")
                                        time.sleep(2)
                                    
                                    Brand = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[1]").text
                                    SKU = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[2]").text
                                    model = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[3]").text
                                    Receiving_item = driver.find_element_by_xpath("(//div[@class='html-content box-content-html'])").text
                                except:
                                    Brand = None
                                    SKU = None
                                    model = None
                                    Receiving_item = None
                            try:
                                Warranty_Type = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[4]").text
                            except:
                                Warranty_Type = None
                            try:
                                Warranty_Period = driver.find_element_by_xpath("(//div[@class='html-content key-value'])[5]").text
                            except:
                                Warranty_Period = None
                            try:
                                rating_out_of_5 = driver.find_element_by_xpath("//span[@class='score-average']").text
                            except:
                                rating_out_of_5 = None
                            yield{
                                    'title':title,
                                    'No of rating':No_of_rating,
                                    'Product_Type':Product_Type,
                                    'image_url':img,
                                    'Product_link':link,
                                    'precentage_off':precentage_off,
                                    'Regular_Price':regular_price,
                                    'stock':stock,
                                    'Discounted_Price':dis,
                                    'content':content,
                                    'Brand':Brand,
                                    'SkU':SKU,
                                    'Model':model,
                                    'Warranty_Type':Warranty_Type,
                                    'Warranty_Period':Warranty_Period,
                                    'Receiving Items':Receiving_item,
                                    'dropship_supplier':dropship_supplier,
                                    'rating_out_of_5':rating_out_of_5,
                            

                            }
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(3)

                except:
                    print("Cannot clicked items")
                    time.sleep(3)
                
                driver.execute_script("window.scrollTo(0, 1200)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(1200, 2400)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(2400, 3600)") 
                time.sleep(2)
                driver.execute_script("window.scrollTo(3600, 4200)") 
                time.sleep(4)
                next = driver.find_element_by_xpath("//li[@title='Next Page']/a[@class='ant-pagination-item-link']")
                if next:
                    ActionChains(driver).move_to_element(next).click().perform()
                    next.click()
                    time.sleep(3)
                else:
                    print("There is a fault")
            else:
                print("There is no button left")
                n = 1
                break