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
import csv

path = which("chromedriver")
options = Options()
options.add_experimental_option("detach", True)
#options.add_argument("--headless")
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=path,options=options)
driver.get("https://www.doximity.com/cv/deepak-ozhathil-md-1")
time.sleep(2)

                
            

print("Profile Pic Link: \n",profile_pic)
print("Name: \n",nam)
print("Catagory: \n",catagory)
print("State: \n",st)
print("Address: \n",address)
print("Phone: \n",phone)
print("fax: \n",fax)
print("Education Training: \n",edu_train)
print("Certifications Licensure: \n",certi_lic)
print("Awards Honors Recognition: \n",awards)
print("Publications Presentations: \n",public_pre)




