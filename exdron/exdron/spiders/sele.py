# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from shutil import which
# from fake_useragent import UserAgent
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# import csv
# import urllib.request


# path = which("chromedriver")
# options = Options()
# options.add_experimental_option("detach", True)
# # options.add_argument("--headless")
# ua = UserAgent()
# userAgent = ua.random
# options.add_argument(f'user-agent={userAgent}')
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(executable_path=path,options=options)
# driver.get("https://www.exdron.co.il/%D7%A7%D7%98%D7%9C%D7%95%D7%92/%D7%93%D7%91%D7%A7%D7%99%D7%9D/%D7%9E%D7%90%D7%99%D7%A6%D7%99%D7%9D-%D7%9C%D7%93%D7%91%D7%A7/")
# time.sleep(2)
# links = driver.find_elements_by_xpath("//h2[@class='pid_title']/a")
# for i in range(0,len(links)):
#     link = driver.find_elements_by_xpath("//h2[@class='pid_title']/a")[i].get_attribute("href")
#     driver.get(link)
#     print(link)
#     time.sleep(2)
#     try:
#         image_name = driver.find_element_by_xpath("//div[@id='product_img']/a/img").get_attribute("alt")
#         # url = driver.find_element_by_xpath("//div[@id='product_img']/a/img").get_attribute("src")
#         absolute_image_name = f"/Users/nabee/projects/e-commerence/exdron/exdron/{image_name}.jpg"
#         Item_name = driver.find_element_by_xpath("//div[@class='page_title td']/h1").text
#         print(Item_name)
#         print(absolute_image_name)
#         driver.back()
#     except:
#         print("Nothing is there")
#         driver.back()
#     # urllib.request.urlretrieve(url, absolute_image_name)
