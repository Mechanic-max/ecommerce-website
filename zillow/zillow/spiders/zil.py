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

class ZilSpider(scrapy.Spider):
    name = 'zil'
    allowed_domains = ['www.zillow.com']
    #start_urls = ['http://www.zillow.com/']

    def start_requests(self):
        yield SeleniumRequest(url='https://www.zillow.com/',callback=self.parse,headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})
 
    def parse(self, response):
        path = which("chromedriver")
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=path)
        driver.set_window_size(1920,1080)
        driver.get(response.url)
        WebDriverWait(driver,5)
        try:
            text_box = driver.find_element_by_xpath("//input[@type='text']")
            text_box.send_keys("Texas")
            WebDriverWait(driver,1)
            btn = driver.find_element_by_xpath("//span[@class='StyledAdornment-c11n-8-23-0__sc-1kerx9v-0 AdornmentRight-c11n-8-23-0__sc-1kerx9v-2 iBKhxd hYxXom ']")
            btn.click()
            WebDriverWait(driver,5)
            driver.implicitly_wait(10)
        except:
            print("there is an error")
        self.html = driver.page_source
        driver.close()
