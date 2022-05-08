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
import sys, unittest, time, datetime
import urllib.request, urllib.error, urllib.parse


class IteSpider(scrapy.Spider):
    name = 'ite'
    allowed_domains = ['www.youtube.com']
    start_urls = ["https://www.youtube.com/channel/UCs7on9W7SIbyO4f-Pb7lgbg/videos"]
    def parse(self,response):
        path = which("chromedriver")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        url = sys.argv[1]
        # channelid = url.split('/')[4]
        driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
        driver.get("https://www.youtube.com/channel/UCs7on9W7SIbyO4f-Pb7lgbg/videos")
        time.sleep(5)
        dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        lastheight = 0

        while True:
            if lastheight == height:
                break
            lastheight = height
            driver.execute_script("window.scrollTo(0, " + str(height) + ");")
            time.sleep(4)
            height = driver.execute_script("return document.documentElement.scrollHeight")

        time.sleep(40)
        self.soup = driver.page_source


        resp = Selector(text=self.soup)
        for i in resp.xpath("//ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']"):
            leng = i.xpath("normalize-space(.//div/ytd-thumbnail/a/div/ytd-thumbnail-overlay-time-status-renderer/span/text())").extract_first()
            yield{
                'Video Title':i.xpath(".//a[@id='video-title']/text()").get(),
                'Number of Viewers':i.xpath(".//div/div[@id='details']/div[@id='meta']/div[@id='metadata-container']/div[@id='metadata']/div[@id='metadata-line']/span[contains(text(),'views')]/text()").get(),
                'Video posting date':i.xpath(".//span[contains(text(),'ago')]/text()").get(),
                'Video Length':leng
            }
