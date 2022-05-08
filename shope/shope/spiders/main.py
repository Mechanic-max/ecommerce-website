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
from scrapy import Request
import selenium.webdriver.support.ui as ui
import time 
from selenium.webdriver.common.action_chains import ActionChains

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['shopee.com.my']
    start_urls = [
        f"https://shopee.com.my/Software-cat.174.242.15006?page={pg}" for pg in range(0,99,1) #default it is all the pages you can set how much pages you want to scrape
    ]
    def start_requests(self):
        for url in self.start_urls: 
            yield SeleniumRequest(url=url,callback=self.parse_item,headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})
 

    def parse_item(self,response):
        path = which("chromedriver")
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True) #uncoment this line and coment the line if you want to see what's gpoing on
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=path,options=chrome_options)
        driver.set_window_size(1920,1080)
        driver.get(response.url)
        driver.implicitly_wait(10)
        try:
            btn = driver.find_element_by_xpath("//button[@class='shopee-button-outline shopee-button-outline--primary-reverse ']")
            if btn:
                btn.click()
            driver.execute_script("window.scrollTo(0, 900)") 
            time.sleep(3)
            driver.execute_script("window.scrollTo(900, 1600)") 
            time.sleep(3)
            driver.execute_script("window.scrollTo(1600, 2500)") 
            time.sleep(4)
        except:
            print("Pop up didn't appear")
    
        time.sleep(1)    
        self.soup = driver.page_source
        driver.close()
        
        resp = Selector(text=self.soup)
        links = resp.xpath("//div[@class='col-xs-2-4 shopee-search-item-result__item']")
        for link in links:
            image_link = link.xpath(".//img[@class='mxM4vG _2GchKS']/@src").get()
            chng_link = link.xpath(".//a/@href").get()
            absolute_url = f"https://shopee.com.my{chng_link}"
            yield SeleniumRequest(url=absolute_url,callback=self.parse,dont_filter=True,meta={'image_link':image_link})
    
    def parse(self, response):
        price,stock,Account_type,sale_pri,Catagory=[],[],[],[],[]
        path = which("chromedriver")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=path,options=chrome_options)
        driver.set_window_size(1920,1080)
        wait = ui.WebDriverWait(driver,100)
        driver.get(response.url)
        driver.implicitly_wait(15)
        try:
            btn = driver.find_element_by_xpath("//button[@class='shopee-button-outline shopee-button-outline--primary-reverse ']")
            if btn:
                btn.click()
                wait           
        except:
            print("There is a no Popup")
        
        time.sleep(1)
        
        bar_check = driver.find_elements_by_xpath("//div[@class='flex items-center _2oeDUI']")
        btn1 = driver.find_elements_by_xpath("//button[@class='product-variation']")
        if len(bar_check)>=2:
            btn_first_option = driver.find_elements_by_xpath("(//div[@class='flex items-center _2oeDUI'])[1]/button[@class='product-variation']")
            if btn_first_option:
                for wsa in btn_first_option:
                    ActionChains(driver).move_to_element(wsa).click().perform()
                    time.sleep(1)
                    cat = driver.find_element_by_xpath("(//div[@class='flex items-center _2oeDUI'])[1]//button[@class='product-variation product-variation--selected']").text
                    Catagory.append(cat)
                    btn_second_option = driver.find_elements_by_xpath("(//div[@class='flex items-center _2oeDUI'])[2]/button[@class='product-variation']")
                    if btn_second_option:
                        for j in btn_second_option:
                            btn_second  = driver.find_element_by_xpath("(//div[@class='flex items-center _2oeDUI'])[2]/button[@class='product-variation']")
                            driver.execute_script("arguments[0].click();", btn_second)
                            time.sleep(1)
                            up_pri = driver.find_element_by_xpath("//div[@class='_3e_UQT']").text
                            price.append(up_pri)
                            up_stk = driver.find_element_by_xpath("(//div[@class='flex items-center']/div)[8]").text
                            stock.append(up_stk)
                            up_Account = driver.find_element_by_xpath("(//div[@class='flex items-center _2oeDUI'])[2]/button[@class='product-variation product-variation--selected']").text
                            Account_type.append(up_Account)
                            
                            sale = driver.find_element_by_xpath("//div[@class='_28heec']").text
                            if sale:
                                sale_pri.append(sale)
                            time.sleep(2)
                            
            self.soup = driver.page_source
            driver.close()
            resp = Selector(text=self.soup)


            store = resp.xpath("//a[@class='_267Jf9']/@href").get()
            store_url = f"https://shopee.com.my{store}"
            yield{
                'title':resp.xpath("normalize-space(//div[@class='attM6y']/span/text())").get(),
                'Catagory':resp.xpath("(//label[@class='_2IW_UG']/text())[2]").get(),
                'Account_type/Product_Type':Account_type,
                'Catagory':Catagory,
                'Content':resp.xpath("normalize-space(//meta[@name='description']/@content)").get(),
                'prdouct type':resp.xpath("(//a[@class='_3YDLCj'])[4]/text()").get(),
                'stock':stock,
                'regular_price':price,
                'sale_price': sale_pri,
                'Wrranty Period':resp.xpath("(//div[@class='aPKXeO']/div)[2]/text()").get(),
                'Wrranty type':resp.xpath("(//div[@class='aPKXeO']/div)[3]/text()").get(),
                'product_url':response.url,
                'images_url': response.meta['image_link'],
                'product_catagory':resp.xpath("//a[@class='_3YDLCj _3LWINq']/text()").getall(),
                'Store_url/dropship_supplier': store_url,
                'Rating out of 5': resp.xpath("//div[@class='OitLRu _1mYa1t']/text()").get(),
                'Rating': resp.xpath("//div[@class='OitLRu']/text()").get(),
                'Sold': resp.xpath("//div[@class='aca9MM']/text()").get(),
                }
            
        
        
        elif len(btn1)>=2:
            for i in btn1:
                ActionChains(driver).move_to_element(i).click().perform()
                time.sleep(2) 
                up_pri = driver.find_element_by_xpath("//div[@class='_3e_UQT']").text
                price.append(up_pri)
                up_stk = driver.find_element_by_xpath("(//div[@class='flex items-center']/div)[6]").text
                stock.append(up_stk)
                btn_txt = driver.find_element_by_xpath("//button[@class='product-variation']").text
                Account_type.append(btn_txt)
                time.sleep(2)
        
 
            self.soup = driver.page_source

            driver.close()
            resp = Selector(text=self.soup)

            store = resp.xpath("//a[@class='_267Jf9']/@href").get()
            store_url = f"https://shopee.com.my{store}"
            yield{
                'title':resp.xpath("normalize-space(//div[@class='attM6y']/span/text())").get(),
                'Catagory':resp.xpath("(//label[@class='_2IW_UG']/text())[2]").get(),
                'Account_type/Product_Type':Account_type,
                'Content':resp.xpath("normalize-space(//meta[@name='description']/@content)").get(),
                'prdouct type':resp.xpath("(//a[@class='_3YDLCj'])[4]/text()").get(),
                'stock':stock,
                'regular_price':price,
                'sale_price': resp.xpath("//div[@class='_28heec']/text()").get(),
                'Wrranty Period':resp.xpath("(//div[@class='aPKXeO']/div)[2]/text()").get(),
                'Wrranty type':resp.xpath("(//div[@class='aPKXeO']/div)[3]/text()").get(),
                'product_url':response.url,
                'images_url': response.meta['image_link'],
                'product_catagory':resp.xpath("//a[@class='_3YDLCj _3LWINq']/text()").getall(),
                'Store_url/dropship_supplier': store_url,
                'Rating out of 5': resp.xpath("//div[@class='OitLRu _1mYa1t']/text()").get(),
                'Rating': resp.xpath("//div[@class='OitLRu']/text()").get(),
                'Sold': resp.xpath("//div[@class='aca9MM']/text()").get(),
            }
            time.sleep(2)
        else:
            self.soup = driver.page_source
            driver.close()
            resp = Selector(text=self.soup)

            store = resp.xpath("//a[@class='_267Jf9']/@href").get()
            store_url = f"https://shopee.com.my{store}"

            yield{
            'title':resp.xpath("normalize-space(//div[@class='attM6y']/span/text())").get(),
            'Catagory':resp.xpath("(//label[@class='_2IW_UG']/text())[2]").get(),
            'Account_type/Product_Type':resp.xpath("//button[@class='product-variation']/text()").get(),
            'Content':resp.xpath("normalize-space(//meta[@name='description']/@content)").get(),
            'prdouct type':resp.xpath("(//a[@class='_3YDLCj'])[4]/text()").get(),
            'stock':resp.xpath("(//div[@class='flex items-center']/div/text())[2]").get(),
            'regular_price':resp.xpath("(//div[@class='flex items-center']/div/text())[1]").get(),
            'sale_price': resp.xpath("//div[@class='_28heec']/text()").get(),
            'Wrranty Period':resp.xpath("(//div[@class='aPKXeO']/div)[2]/text()").get(),
            'Wrranty type':resp.xpath("(//div[@class='aPKXeO']/div)[3]/text()").get(),
            'product_url':response.url,
            'images_url': response.meta['image_link'],
            'product_catagory':resp.xpath("//a[@class='_3YDLCj _3LWINq']/text()").getall(),
            'Store_url/dropship_supplier': store_url,
            'Rating out of 5': resp.xpath("//div[@class='OitLRu _1mYa1t']/text()").get(),
            'Rating': resp.xpath("//div[@class='OitLRu']/text()").get(),
            'Sold_amounts': resp.xpath("//div[@class='aca9MM']/text()").get(),
        }