import requests
from requests.structures import CaseInsensitiveDict
import time 
import csv
from datetime import datetime
import ast

count = 0
currentdate = datetime.today().strftime('%Y-%m-%d')
epochtime = round(time.time() * 1000)
print("Sending request to server ...")
url = "https://irs.tools.investis.com/Clients/HistoryDataForChartV3.ashx?symbol=TRYG.NAV&WithVolume=true&IsMain=true&address=clients/dk/trygvesta_nav/minichart/default.aspx&nocache=1&{}&_="+str(epochtime)

headers = CaseInsensitiveDict()
headers["Connection"] = "keep-alive"
headers["sec-ch-ua"] = "'Microsoft Edge';v='93', ' Not;A Brand';v='99', 'Chromium';v='93'"
headers["DNT"] = "1"
headers["sec-ch-ua-mobile"] = "?0"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38"
headers["Content-Type"] = "application/json"
headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
headers["X-Requested-With"] = "XMLHttpRequest"
headers["sec-ch-ua-platform"] = "'Windows'"
headers["Sec-Fetch-Site"] = "same-origin"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Dest"] = "empty"
headers["Referer"] = "https://irs.tools.investis.com/Clients/dk/trygvesta_NAV/Minichart/default.aspx?culture=en-US&nocache=1"
headers["Accept-Language"] = "en-US,en;q=0.9"
headers["Cookie"] = "AWSELBCORS=FF51515F140E3F2AABAE53DD54ABEEEC4393737C1794C0749111651F1D79ABF757BA7D3B7370CBA02843310CD7D9A99C30E9DADB6EAD4362FD86109058A1E8175012ECA6E4"

print("Processing the Request ...")
resp = requests.get(url, headers=headers)
datalist = []
data = resp.json()
data = ast.literal_eval(data["Data"])
for detail in data:
    datalist.append([currentdate,detail[0],detail[1]])
print("Generating the Data ...")
filename = str(currentdate)+".csv"
with open(filename, 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["scrape_date","timestamp","NAV"])
    writer.writerows(datalist)
    count = count+1
    print("No of rows are saved are:",count)
print(f"Generated the Data at {currentdate} ...")