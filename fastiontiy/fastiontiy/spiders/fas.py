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



class FasSpider(scrapy.Spider):
    name = 'fas'
    allowed_domains = ['www.fashiontiy.com']
    custon_setting={
        'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
    }

    def start_requests(self):
        yield SeleniumRequest(url='https://www.fashiontiy.com/men-tops.html',callback=self.parse)

    
    def aloo():
        coli_item = driver.find_elements_by_xpath("//div[@class='color_colors']/div")
        for i in range(0,len(coli_item)):
            col = driver.find_element_by_xpath("//div[@class='base_key_value size_title_left']/span[@class='notranslate']").text
            color.append(col)
            sizes = driver.find_elements_by_xpath("//div[@class='size_list notranslate']/div/span[@class='size_item_name ']")
            for j in range(0,len(sizes)):
                sizes_avaiable = driver.find_elements_by_xpath("//div[@class='size_list notranslate']/div/span[@class='size_item_name ']")[j].text
                siz.append(sizes_avaiable)
                stock = driver.find_elements_by_xpath("//div[@class='size_list notranslate']/div/span[not(contains(@class,'size_item_name '))]")[j].text
                stocks.append(stock)
            btn = driver.find_elements_by_xpath("//div[@class='color_colors']/div")[i]
            btn.click()
            time.sleep(4)
        
        self.html = driver.page_source 
        resp = Selector(text=self.html)
        no_of_piece_1 = resp.xpath("(//div[@class='price_item']/p[@class='price_desc'])[1]/text()").extract_first()
        no_of_piece_2 = resp.xpath("(//div[@class='price_item']/p[@class='price_desc'])[2]/text()").extract_first()
        no_of_piece_3 = resp.xpath("(//div[@class='price_item']/p[@class='price_desc'])[3]/text()").extract_first()
        yield{
            'id': resp.xpath("//div[@class='right_title notranslate']/text()").get(),
            'Name': resp.xpath("//div[@class='right_desc']/span/text()").get(),
            'Min order Requirenment': resp.xpath("//div[@class='right_moq base_key_value']/span[@class='notranslate']/text()").get(),
            f'{no_of_piece_1}' : resp.xpath("(//div[@class='price_item']/p[@class='price_title notranslate'])[1]/text()").get(),
            f'{no_of_piece_2}' : resp.xpath("(//div[@class='price_item']/p[@class='price_title notranslate'])[2]/text()").get(),
            f'{no_of_piece_3}' : resp.xpath("(//div[@class='price_item']/p[@class='price_title notranslate'])[3]/text()").get(),
            'images_url' : resp.xpath("//div[@class='detail_left']//img/@src").getall(),
            'color': color,
            'Size': siz,
            'Stock': stocks,
            'Gross_Weight' : resp.xpath("(//div[@class='base_key_value']/span[not(contains(@class,'key'))])[1]/text()").get(),
            'Material' : resp.xpath("(//div[@class='base_key_value']/span[not(contains(@class,'key'))])[2]/text()").get(),
            'Asian Size' : resp.xpath("(//div[@class='base_key_value']/span[not(contains(@class,'key'))])[3]/text()").get(),
        }
    
    
    def parse(self, response):
        path = which("chromedriver")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
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
        links = driver.find_elements_by_xpath("//div[@class='list_products']/div//a[@class='product_infos_2 notranslate']")
        for i in range(0,len(links)):
            link = driver.find_elements_by_xpath("//div[@class='list_products']/div//a[@class='product_infos_2 notranslate']")[i].get_attribute("href")
            driver.get(link)
            time.sleep(2)
            aloo()
            driver.back()
            time.sleep(2)
            