from tkinter import N
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
import time
from scrapy.selector import Selector
import csv
import re

class Horse():

    count = 0
    year = 2022
    def start(self):
        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')

        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        

    def target_url(self):
        for i in range(1126044,1030000,-1):
            ul = f"https://horsetourneys.com/leaderboard/contest/{i}"
            try:
                self.driver.get(ul)
            except:
                self.driver.close()
                self.start()
                self.driver.get(ul)

            time.sleep(5)
            self.scrap(ul)
        
    def scrap(self,link):
        html = self.driver.page_source
        resp = Selector(text=html)
        
        
        link = str(link)
        
        day = resp.xpath("normalize-space(//div[@class='date']/div[@class='date-day']/text())").extract_first()
        month =resp.xpath("normalize-space(//div[@class='date']/div[@class='date-month']/text())").extract_first()
        if month == 'Dec':
            self.year = self.year-1
        
        date = f"{day}-{month}-{self.year}"
        if (day == '' or day == None) and (month == '' or month == None):
            date = ''
        
        winning = ''
        contest_id = re.findall(r"\b(\w+)$",link)
        contest_id =str(contest_id)
        contest_id = contest_id.replace('[','')
        contest_id = contest_id.replace(']','')
        contest_id = contest_id.replace('"','')
        contest_id = contest_id.replace("'","")
        contest_id = contest_id.replace(","," ")
        contest_id = contest_id.strip()

        qualifer_or_cash = ""
        qualifer_cash = resp.xpath("normalize-space(//h1[contains(text(),'QUALIFIER')]/text())").extract_first()
        if qualifer_cash:
            qualifer_or_cash = "Qualifer"
        else:
            qualifer_or_cash = "Cash"


        game = ""
        track_total_prize_game_type = resp.xpath("normalize-space(//div[@class='type-tournament']/h1/text())").extract_first()
        track_total_prize_game_type = str(track_total_prize_game_type)
        if 'WINNER' in track_total_prize_game_type:
            winning = re.findall(r'\$.+\bWINNER', track_total_prize_game_type)
            winning = str(winning)
            winning = winning.replace('[','')
            winning = winning.replace(']','')
            winning = winning.replace('"','')
            winning = winning.replace("'","")
            winning = winning.replace(",","")
            winning = winning.replace("WINNER","")
            winning = winning.strip()
            print("winning",winning)
        
        if 'Runs w/ 3' in track_total_prize_game_type:
            game = 'Runs w/ 3'
            track_total_prize_game_type = track_total_prize_game_type.replace(game,"")
        track = re.findall(r'^\w.+?-',track_total_prize_game_type)
        track =str(track)
        track = track.replace('[','')
        track = track.replace(']','')
        track = track.replace('"','')
        track = track.replace("'","")
        track = track.replace(",","")

        
        track_total_prize_game_type = track_total_prize_game_type.replace(track,"")
        track = track.replace("-","")
        track = track.strip()
        if "Head-to-Head" in track_total_prize_game_type:
            game = "Head-to-Head"
            track_total_prize_game_type = track_total_prize_game_type.replace(game,"")

        total_prize = re.findall(r'\$\w+.+\d',track_total_prize_game_type)
        total_prize =str(total_prize)
        total_prize = total_prize.replace('[','')
        total_prize = total_prize.replace(']','')
        total_prize = total_prize.replace('"','')
        total_prize = total_prize.replace("'","")
        total_prize = total_prize.replace(",","")
        total_prize = total_prize.replace("-","")
        total_prize = total_prize.replace("    "," ")
        total_prize = total_prize.strip()
        track_total_prize_game_type = track_total_prize_game_type.replace(total_prize,"")
        type = track_total_prize_game_type.replace("-","")
        type = type.replace("    "," ")
        type = type.replace(",","")
        type = type.replace(total_prize,"")
        type = type.strip()

        entry_fee = ''
        full_description = resp.xpath("//div[@class='prizes-info']/text()").getall()
        full_description = str(full_description)
        full_description = full_description.replace('[','')
        full_description = full_description.replace(']','')
        full_description = full_description.replace('"','')
        full_description = full_description.replace("'","")
        full_description = full_description.replace(",","")
        full_description = full_description.strip()
        if 'breakage' in full_description:
            entry_fee = re.findall(r'\$\d+\s\bbreakage\b',full_description)
            entry_fee =str(entry_fee)
            entry_fee = entry_fee.replace('[','')
            entry_fee = entry_fee.replace(']','')
            entry_fee = entry_fee.replace('"','')
            entry_fee = entry_fee.replace("'","")
            entry_fee = entry_fee.replace(",","")
            entry_fee = entry_fee.replace("breakage","")
            entry_fee = entry_fee.strip()
        
        if winning == None or winning == '':
            if 'Winner' in full_description:
                winning = re.findall(r'\$\w+.\d\s',full_description)
                winning = str(winning)
                winning = winning.replace('[','')
                winning = winning.replace(']','')
                winning = winning.replace('"','')
                winning = winning.replace("'","")
                winning = winning.replace(",","")
                winning = winning.strip()
            
            elif '1st:' in full_description:
                winning = re.findall(r'\$\w+\s',full_description)
                winning = str(winning)
                winning = winning.replace('[','')
                winning = winning.replace(']','')
                winning = winning.replace('"','')
                winning = winning.replace("'","")
                winning = winning.replace(",","")
                winning = winning.strip()
            
            else:
                winning = ''
        
        winning_n = ''
        entry_fee_n = ''
        if game == "Head-to-Head":
            if winning == '$40':
                entry_fee = '$22'
            elif winning == '$100':
                entry_fee = '$55'
            elif winning == '$200':
                entry_fee = '$110'
            elif winning == '$400':
                entry_fee = '$218'
            elif winning == '$800':
                entry_fee = '$430'
            elif winning == '$1500':
                entry_fee = '$795'
            elif winning == '$3000':
                entry_fee = '$1585'
            else:
                entry_fee = '$0'
       
        print(entry_fee)
        net = 0
        try:
            if winning == None or winning == '':
                winning_n =0
            else:
                winning_n = winning.replace('$','')
                winning_n = int(winning_n)
            if entry_fee == None or entry_fee == '' or entry_fee =="":
                entry_fee_n = 0
            else:
                
                entry_fee_n = entry_fee.replace('$','')
                entry_fee_n = int(entry_fee_n)
            net = winning_n-entry_fee_n
        except:
            None
        
        
        
        
        rank = ''
        player = ''
        earning = ''
        entry =''
        pagee_check = resp.xpath("//div[@id='leaderboard-pager']/span/a[@href]").getall()
        print("pagee_check",pagee_check)
        if pagee_check != []:
            if len(pagee_check) != 0:
                for io in range(1,len(pagee_check)+1):
                    print("Number of pages",io,len(pagee_check))
                    page_xpath = f"//div[@id='leaderboard-pager']/span/a[@href='{io}']"
                    self.driver.find_element_by_xpath(page_xpath)
                    button = self.driver.find_element_by_xpath(page_xpath)
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(3)
                    data = resp.xpath("//table[@id='leaderboard']/tbody/tr[@rel]")
                    print("length",len(data))
                    if len(data) != 0:
                        for i in range(1,len(data)+1):
                            rank = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[1]/text())").extract_first()
                            player_name = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[2]/text())").extract_first()
                            player_name = str(player_name)
                            player = re.findall(r'^\w.+?-',player_name)
                            player = str(player)
                            player = player.replace('[','')
                            player = player.replace(']','')
                            player = player.replace('"','')
                            player = player.replace("'","")
                            player = player.replace(",","")
                            entry = player_name.replace(player,'')
                            entry = entry.replace('Entry','')
                            entry = entry.strip()
                            player = player.replace("-","")
                            player = player.strip()


                            earning = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[3]/text())").extract_first()
                            self.print_save(contest_id,date,qualifer_or_cash,game,track,total_prize,type,entry_fee,full_description,rank,player,entry,earning,winning,net,link)
                    else:
                        self.print_save(contest_id,date,qualifer_or_cash,game,track,total_prize,type,entry_fee,full_description,rank,player,entry,earning,winning,net,link)
        else:
            data = resp.xpath("//table[@id='leaderboard']/tbody/tr[@rel]")
            print("length",len(data))
            if len(data) != 0:
                for i in range(1,len(data)+1):
                    rank = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[1]/text())").extract_first()
                    player_name = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[2]/text())").extract_first()
                    player_name = str(player_name)
                    player = re.findall(r'^\w.+?-',player_name)
                    player = str(player)
                    player = player.replace('[','')
                    player = player.replace(']','')
                    player = player.replace('"','')
                    player = player.replace("'","")
                    player = player.replace(",","")
                    entry = player_name.replace(player,'')
                    entry = entry.replace('Entry','')
                    entry = entry.strip()
                    player = player.replace("-","")
                    player = player.strip()


                    earning = resp.xpath(f"normalize-space(//table[@id='leaderboard']/tbody/tr[@rel][{i}]/td[3]/text())").extract_first()
                    self.print_save(contest_id,date,qualifer_or_cash,game,track,total_prize,type,entry_fee,full_description,rank,player,entry,earning,winning,net,link)
            else:
                self.print_save(contest_id,date,qualifer_or_cash,game,track,total_prize,type,entry_fee,full_description,rank,player,entry,earning,winning,net,link)  
            
            


    def print_save(self,contest_id,date,qualifer_or_cash,game,track,total_prize,type,entry_fee,full_description,rank,player,entry,earning,winning,net,link):
        print()
        print("contest_id:",contest_id)
        print("date:",date)
        print("qualifer_or_cash:",qualifer_or_cash)
        print("game:",game)
        print("track:",track)
        print("total_prize:",total_prize)
        print("type:",type)
        print("entry_fee:",entry_fee)
        print("full_description:",full_description)
        print("rank:",rank)
        print("player:",player)
        print("entry:",entry)
        print("earning:",earning)
        print("winning:",winning)
        print("net:",net)
        print("url:",link)
        print()
        with open("Dataset_sample.csv",'a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            if self.count == 0:
                writer.writerow(['contest_id','date','game','type','track','total_prize','rank','player','entry','earning','full_description','entry_fee','qualifer_or_cash','winning','net','link'])
            writer.writerow([contest_id,date,game,type,track,total_prize,rank,player,entry,earning,full_description,entry_fee,qualifer_or_cash,winning,net,link])
            self.count = self.count + 1
            print("Data saved in CSV: ",self.count)  

    def close(self):
        self.driver.close()
if __name__ == '__main__':
    scraper = Horse()
    scraper.start()
    scraper.target_url()

    scraper.close()