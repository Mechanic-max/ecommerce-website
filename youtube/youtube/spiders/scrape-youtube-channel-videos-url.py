import sys, unittest, time, datetime
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

path = which("chromedriver")
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
url = sys.argv[1]
channelid = url.split('/')[4]
driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
driver.get(url)
time.sleep(5)
dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
height = driver.execute_script("return document.documentElement.scrollHeight")
lastheight = 0

while True:
	if lastheight == height:
		break
	lastheight = height
	driver.execute_script("window.scrollTo(0, " + str(height) + ");")
	time.sleep(2)
	height = driver.execute_script("return document.documentElement.scrollHeight")

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
for i in user_data:
	print(i.get_attribute('href'))
	link = (i.get_attribute('href'))
	f = open(channelid+'-'+dt+'.list', 'a+')
	f.write(link + '\n')
f.close