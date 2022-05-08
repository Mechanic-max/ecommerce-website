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
from pandas import DataFrame

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
driver.get("https://www.doximity.com/directory/md/location/new-mexico")
time.sleep(2)


def moli():
    time.sleep(2)
    nam,st,edu_train,certi_lic,awards,public_pre = [],[],[],[],[],[]
    try:
        names = driver.find_elements_by_xpath("//h1/span[@id='user_full_name']/span")
        for i in range(0,len(names)):
            name = driver.find_elements_by_xpath("//h1/span[@id='user_full_name']/span")[i].text
            nam.append(name)
    except:
        print("Name is not avaiable")
        nam = None

    try:
        profile_pic = driver.find_element_by_xpath("//div[@class='profile-photo']/img").get_attribute("src")
    except:
        profile_pic = None

    try:
        catagory = driver.find_element_by_xpath("//a[@class='profile-head-subtitle']").text
    except:
        catagory = None

    try:
        state = driver.find_elements_by_xpath("//span[@class='profile-head-subtitle']/span/a")
        for i in range(0,len(state)):
            stat = driver.find_elements_by_xpath("//span[@class='profile-head-subtitle']/span/a")[i].text
            st.append(stat)
    except:
        print("State is not avaiable")
        st = None

    try:
        address= driver.find_element_by_xpath("//span[@class='black profile-contact-labels-wrap']").text
    except:
        address = None

    try:
        phone = driver.find_element_by_xpath("//div[@class='office-info-telephone']//span[@class='black']").text
    except:
        phone = None

    try:
        fax = driver.find_element_by_xpath("//div[@class='office-info-fax']//span[@class='black']").text
    except:
        fax = None

    try:
        education_training = driver.find_elements_by_xpath("//ul[@class='profile-sectioned-list training']/li/div[@class='profile-section-wrapper-text']/span")
        for i in range(0,len(education_training)):
            edtrain = driver.find_elements_by_xpath("//ul[@class='profile-sectioned-list training']/li/div[@class='profile-section-wrapper-text']/span")[i].text
            edu_train.append(edtrain)
    except:
            print("Education & Training is not avaiable")
            edu_train = None

    try:
        Certifications_Licensure = driver.find_elements_by_xpath("//section[@class='certification-info']/ul[@class='profile-sectioned-list']/li/div/span")
        for i in range(0,len(Certifications_Licensure)):
            ctli = driver.find_elements_by_xpath("//section[@class='certification-info']/ul[@class='profile-sectioned-list']/li/div/span")[i].text
            certi_lic.append(ctli)
    except:
        print("Certifications & Licensure is not avaiable")
        certi_lic = None

    try:
        Awards_Honors_Recognition = driver.find_elements_by_xpath("//section[@class='award-info']/ul[@class='profile-sectioned-list']/li/span[@class]")
        for i in range(0,len(Awards_Honors_Recognition)):
            aw_ho_re = driver.find_elements_by_xpath("//section[@class='award-info']/ul[@class='profile-sectioned-list']/li/span")[i].text
            awards.append(aw_ho_re)
    except:
        try:
            aw = driver.find_element_by_xpath("//section[@class='award-info']/ul[@class='profile-sectioned-list']/li/span").text
            awards.append(aw)
        except:    
            print("Awards, Honors, & Recognition is not avaiable")
            awards = None

    try:
        Publications_Presentations = driver.find_elements_by_xpath("//ul[@class='profile-sectioned-list publications sec_pubmed_articles']/li[not(contains(@style,'display:none'))]/span/a/div[@class='list-section-publication-title']")
        for i in range(0,len(Publications_Presentations)):
            pp = driver.find_elements_by_xpath("//ul[@class='profile-sectioned-list publications sec_pubmed_articles']/li[not(contains(@style,'display:none'))]/span/a/div[@class='list-section-publication-title']")[i].text
            public_pre.append(pp)
    except:
        print("Publications & Presentations is not avaiable")
        public_pre = None
        
    with open('New_Mexico.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Profile Pic Link", "Name", "Catagory","State","Address","Phone","fax","Education_Training","Certifications Licensure","Awards Honors Recognition","Publications Presentations"])
        writer.writerow([profile_pic, nam, catagory,st,address,phone,fax,edu_train,certi_lic,awards,public_pre])
        print("Data Saved in CSV")
    driver.back()
    time.sleep(0.5)

def aloo():
    lo = driver.find_elements_by_xpath("//ul[@class='list-4-col']/li/a")
    for xli in range(0,len(lo)):
        lo = driver.find_elements_by_xpath("//ul[@class='list-4-col']/li/a")[xli].get_attribute("href")
        driver.get(lo)
        time.sleep(0.5)
        moli()    
    try:
        next_pg = driver.find_element_by_xpath("//a[@class='next_page']").get_attribute("href")
        if next_page:
            absolute_next_pg = f"https://www.doximity.com/{next_page}"
            driver.get(absolute_next_pg)
            time.sleep(0.5)
            moli()
            driver.back()
            time.sleep(0.5)
            driver.back()
            time.sleep(0.5)
    except:
        print("There are no more pages")
        driver.back()
        time.sleep(1)


def gobi():
    ls = driver.find_elements_by_xpath("//ul[@class='list-4-col cities']/li/a")
    for xlo in range(0,len(ls)):
        ls = driver.find_elements_by_xpath("//ul[@class='list-4-col cities']/li/a")[xlo].get_attribute("href")
        driver.get(ls)
        time.sleep(4)
        try:
            aloo()
        except:
            print("No People are Available")
            driver.back()
            time.sleep(0.5)
    
    next_page = driver.find_element_by_xpath("//a[@class='next_page']").get_attribute("href")
    if next_page:
        absolute_next_page = f"https://www.doximity.com/{next_page}"
        driver.get(absolute_next_page)
        time.sleep(0.5)
        gobi()


# print("Profile Pic Link: \n",profile_pic)
# print("Name: \n",nam)
# print("Catagory: \n",catagory)
# print("State: \n",st)
# print("Address: \n",address)
# print("Phone: \n",phone)
# print("fax: \n",fax)
# print("Education Training: \n",edu_train)
# print("Certifications Licensure: \n",certi_lic)
# print("Awards Honors Recognition: \n",awards)
# print("Publications Presentations: \n",public_pre)


try:
    gobi()    
except:
    # driver.close()
    print("Wait")