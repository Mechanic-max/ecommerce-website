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


class CitySpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['www.selfstorage.com']
    custom_settings = {
    'FEED_EXPORT_FIELDS': ["Name", "Phone", "Street", "State","Facility_Amenities", "Office_hours", "Access_Hours","images","images_url","img_url_name","size", "catagory", "discount", "price","description","Size_Catagory_Discount_Price_description"],
  }
    def start_requests(self):
        with open("/Users/nabee/projects/e-commerence/selfstorage/selfstorage/spiders/input.csv", 'r') as input_file:
            for zip_code in input_file:
                zip1 = zip_code.strip()
                url_main = f"https://www.selfstorage.com/search?location={zip1}"
                yield scrapy.Request(url=url_main,callback=self.parse_item)
    
    def parse_item(self, response):
        next_page = response.xpath("//a[@rel='nofollow' and @class='ss-link pagination-link']/span[contains(text(),'Next')]/parent::*/@href").get()
        absolute_next_page = response.urljoin(next_page)
        links = response.xpath("//div[@class='search-results']/div")

        for link in links:
            url = link.xpath(".//div[@class='facility-card-content']/a/@href").get()
            other_url = link.xpath(".//div/div[@class='facility-details']/a/@href").get()
            if url:
                absolute_url = response.urljoin(url)
                yield SeleniumRequest(url=absolute_url,callback=self.parse)
        
            if other_url:
                absolute_url_2 = response.urljoin(other_url)
                yield scrapy.Request(url=absolute_url_2,callback=self.joint_item)
        
        if next_page:
            yield scrapy.Request(url=absolute_next_page,callback=self.parse_item)

    def joint_item(self, response):      
        images_url = response.xpath("//h1/a")
        img_url_name = response.xpath("//h1/a")
        Name = response.xpath("(//h1[@class='facility-name ss-type ss-type-large']/text())[1]").get(),
        Street = response.xpath("//span[@class='street']/text()").get(),
        State = response.xpath("//span[@itemprop='addressLocality' and @class='city' or @class='state' or @class='zip']/text()").getall(),
        Phone = None
        Facility_Amenities = None
        Office_hours = None
        Access_Hours = None
        size = None
        catagory = None
        discount = None
        price = None
        description = None
        items = None
        yield{
            'Name': Name,
            'Street': Street,
            'State': State,
            'Phone': Phone,
            'Facility Amenities': Facility_Amenities,
            'images_url':images_url,
            'img_url_name':img_url_name,
            'Office_hours':Office_hours,
            'Access_Hours':Access_Hours,
            'size':size,
            'catagory':catagory,
            'discount':discount,
            'price':price,
            'description':description,
            'Size_Catagory_Discount%_Price_Di':items,
        }
    
    def parse(self, response):
        size,discount,price,catagory,description=[],[],[],[],[]
        items=[]
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

        btn = driver.find_element_by_xpath("//button[@class='amenities-learn-more ss-link ss-link-secondary']")
        btn.click()
        time.sleep(1.5)

        self.html = driver.page_source 
        resp = Selector(text=self.html)
        driver.close()
        units = resp.xpath("//div[@class='unit-details']")
        for i in units:
            siz = i.xpath(".//div/div[@class='facility-unit-size']/span[@class='unit-size ss-type ss-type-last ss-type-medium']/text()").extract_first()
            cat = i.xpath(".//div/div[@class='facility-unit-size']/span[@class='unit-type ss-type ss-type-last']/text()").extract_first()
            dis = i.xpath(".//div/div[@class='amenities-list']/p/text()").extract_first()
            pri = i.xpath(".//div[@class='facility-unit-price-and-reserve']/div[@class='facility-unit-price']/span[contains(text(),'$')]/text()").extract_first()
            descript = i.xpath(".//div[@class='facility-unit-amenities']/div[@class='amenities-list']/ul/child::li/text()").getall()
            size.append(siz)
            catagory.append(cat)
            discount.append(dis)
            price.append(pri)
            description.append(descript)
            items.append(siz)
            items.append(cat)
            items.append(dis)
            items.append(pri)
            items.append(descript)

        loader = ItemLoader(item=SelfstorageItem())   

        Name = resp.xpath("//div[@class='page-group']/h1/text()").get(),
        Street = resp.xpath("//span[@class='address ss-type']/span[contains(@class,'')]/span/text()").get(),
        State = resp.xpath("//span[@class='address ss-type']/span[contains(@class,'')]/text()").getall(),
        Phone = resp.xpath("//p[@class='facility-contact ss-type']/a[@class='ss-link ss-link-secondary']/text()").extract_first(),
        images_url =  resp.xpath("//div[@class='ss-slider facility-image-carousel']//img[@class='facility-image']/@src").getall()
        img_url_name =  resp.xpath("//div[@class='ss-slider facility-image-carousel']//img[@class='facility-image']/@alt").getall()
        Facility_Amenities = resp.xpath("//div[@class='amenities-lists']//text()").getall(),
        Office_hours = resp.xpath("(//div[@class='facility-hours-list'])[1]/@datetime").get(),
        Access_Hours = resp.xpath("(//div[@class='facility-hours-list'])[2]/@datetime").get(),
        
        loader.add_value('Name', Name)
        loader.add_value('Street', Street)
        loader.add_value('State', State)
        loader.add_value('Phone', Phone)
        loader.add_value('images_url', images_url)
        loader.add_value('img_url_name', img_url_name)
        loader.add_value('Facility_Amenities', Facility_Amenities)
        loader.add_value('Office_hours', Office_hours)
        loader.add_value('Access_Hours', Access_Hours)
        loader.add_value('size', size)
        loader.add_value('catagory', catagory)
        loader.add_value('discount', discount)
        loader.add_value('price', price)
        loader.add_value('description', description)
        loader.add_value('Size_Catagory_Discount_Price_description', items)
        
        yield loader.load_item()
        
        
        