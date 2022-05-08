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

count = 0
ul = "https://www.zulutrade.com/traders/all"
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
driver.get(ul)
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Trader","Amount Following","Investors","Live Investor Profit","ROI"])

time.sleep(4)

time.sleep(2)
try:
    driver.find_element_by_xpath("//div[@class='cookie-policy-wrapper slds-clearfix slds-grid slds-wrap']/button[@class='slds-button slds-button--icon']").click()
    time.sleep(1)
except:
    print("Pop up didn't appear")
time.sleep(2)
n = 0
# while n ==0:
#     try:
#         driver.find_element_by_xpath("//button[@class='slds-button slds-button--inverse']").click()
#         time.sleep(10)
#         n=0
#     except:
#         print("Button didn't Appear")
#         n=1

for i in range(0,2):
    try:
        driver.find_element_by_xpath("//button[@class='slds-button slds-button--inverse']").click()
        time.sleep(10)
    except:
        print("Button didn't Appear")

Amount_Following = driver.find_elements_by_xpath("//span[contains(text(),'ROI')]//parent::div//parent::td")
print("Total Records Will be:",len(Amount_Following))

trade = driver.find_elements_by_xpath("//a[@class='text-main zlds-link--brand']/h4")
for i in range(0,len(trade)):
    try:
        trade = driver.find_elements_by_xpath("//a[@class='text-main zlds-link--brand']/h4")[i].text
    except:
        trade = None
    try:
        Live_Investor = driver.find_elements_by_css_selector("div.zlds-text-color--brand")[i].text
    except:
        Live_Investor = None
    try:
        Amount_Following = driver.find_elements_by_xpath("//div[contains(text(),'Amount Following')]/following-sibling::div")[i].text
    except:
        Amount_Following = None
    try:
        Investor = driver.find_elements_by_xpath("//div[contains(text(),'Investors')]//parent::td/span")[i].text
    except:
        Investor = None
    try:
        ROI = driver.find_elements_by_xpath("//span[contains(text(),'ROI')]//parent::div//parent::td")[i].text
        try:
            ROI = str(ROI)
            ROI = ROI.replace("ROI","")
            ROI = ROI.strip()
        except:
            ROI = driver.find_elements_by_xpath("//span[contains(text(),'ROI')]//parent::div//parent::td")[i].text
    except:
        ROI = None
        
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([trade,Amount_Following,Investor,Live_Investor,ROI])
        count = count + 1
        print("Data Saved in CSV", count)

    
driver.close()