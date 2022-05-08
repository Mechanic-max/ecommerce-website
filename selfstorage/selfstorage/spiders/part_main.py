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
from selfstorage.items import SelfstorageItem
from scrapy.loader import ItemLoader


class PartmainSpider(scrapy.Spider):
    name = 'partmain'
    allowed_domains = ['www.selfstorage.com']
    custom_settings = {
    'FEED_EXPORT_FIELDS': ["Name", "Phone", "Street", "State","Facility_Amenities", "Office_hours", "Access_Hours","images","images_url","img_url_name","size", "catagory", "discount", "price","description","Size_Catagory_Discount_Price_description"],
  }
    def start_requests(self):
        yield SeleniumRequest(url="https://www.selfstorage.com/self-storage/tennessee/#places",callback=self.parse)

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
        time.sleep(2)
        btn = driver.find_element_by_xpath("//a[@class='ss-link expanded-cities']")
        btn.click()
        time.sleep(1)
        self.html = driver.page_source 
        resp = Selector(text=self.html)
        driver.close()
        for link in resp.xpath(" (//div[@class='page-container']/div[@class='page-section'])[3]//li/span/a[@class='ss-link']"):
            url = response.urljoin(link.xpath(".//@href").get())
            absolute_url = response.urljoin(url)
            yield {
                'url':absolute_url
            }  