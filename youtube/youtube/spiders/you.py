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

class YouSpider(scrapy.Spider):
    name = 'you'
    allowed_domains = ['www.youtube.com']
    def start_requests(self):
        with open("/Users/nabee/projects/e-commerence/youtube/youtube/spiders/url_folder/Little Baby Bum - Nursery Rhymes & Kids Songs.csv", 'r') as input_file:
            for urls in input_file:
                url = urls.strip()
                yield SeleniumRequest(url=url,callback=self.parse)
# 
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
        time.sleep(1.5)
        name = driver.find_element_by_xpath("//h1[@class='title style-scope ytd-video-primary-info-renderer']").text
        views = driver.find_element_by_xpath("//span[@class='view-count style-scope ytd-video-view-count-renderer']").text
        date = driver.find_element_by_xpath("//div[@id='date']/yt-formatted-string").text
        length = driver.find_element_by_xpath("//span[@class='ytp-time-duration']").text
        yield{
            'Video Title':name,
            'Number of Viewers':views,
            'Video posting date':date,
            'Video Length':length,
        }
        driver.close()
