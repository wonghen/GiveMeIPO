import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search
import numpy as np

base_site = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=s-1&owner=include&count=100&action=getcurrent"
response = requests.get(base_site)
html = response.content
soup = bs(html, "lxml")
table = soup.find_all('table')[6]
ListOfCompanies = []

with open ('sec.goc.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))
    
for i in table.find_all('tr'):
    line = i.find_all('td')
    if (len(line) > 2):
        text = line[2].get_text()
        if (not text.startswith("[Amend]") and not text.startswith("General form") and not text.startswith("Registration")):
            ListOfCompanies.append(text.split(" (")[0])
            print(text.split(" (")[0])
            
 print(ListOfCompanies)
 
 def google_scrape(url):
    #thepage = urllib3.urlopen(url)
    soup = bs(requests.get(url).content, "html.parser")
    return soup.title.text

csvTable = []

for com in ListOfCompanies:
    i = 1
    lastUrl = "  "
    print ("Company: "+com)
    row = []
    row.append(com)
    csvTable.append(row)
    for url in search(com, tld = 'com', num=5, stop=15):
        if (url.startswith(lastUrl) or i > 5):
            continue
        #a = google_scrape(url)
        #print (str(i) + ". " + a)
        print (str(i) + ". " + url)
        row.append(url)
        lastUrl = url
        print (" ")
        i += 1
        
np.savetxt("GiveMeIPO.csv", csvTable, delimiter=", ", fmt='% s')
