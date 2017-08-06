# !Python2
# -------------------------
# Author: Lorenzo Basso
# Script type: web-html scraper
# -------------------------
# date: 
# v1: 23/07/2017
# -------------------------
# execution timing: 
# 3m31s or 211.5s on Ubuntu 14.04, DELL Inspiron 7548, i7-5500U CPU, 4 x 2.40GHz
# 437 entries
# -------------------------


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from datetime import timedelta,datetime         # needed for timing
from bs4 import BeautifulSoup			# html scraper
import requests					# to access url
import csv					# export to csv file 

# --------------------------
# start
start_time = datetime.now()
print('start = ',start_time)

# set url
url='https://n1a.goexposoftware.com/events/lva16/goExpo/exhibitor/listExhibitorProfiles.php'
page = requests.get(url)

#scrape with bf4
soup = BeautifulSoup(page.content, 'html.parser')


# define function to extract string content between 2 markers 
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

################################################################
# 1 -------  get all links to individual dealers pages from homepage

# get all links

pagelist = []
for link in soup.find_all('a'):
    pagelist.append(link.get('href')) 

# distill the actual url
pages=[]
for item in pagelist[16:]:
    if item.find("exhibitor/viewExhibitorProfile.php")!=-1:
        pages.append(item)


################################################################
# 2 -------  get content from each sub-page, print it on screen and save it on csv file 


with open(r'document.csv', 'wab') as f:		#create document.csv if not exist or overwrite if exists already, append data
    writer = csv.writer(f)
    for page in pages:
	print("-------------------------------------")
        url='https://n1a.goexposoftware.com/events/lva16/goExpo/'+page
        print("url = ",url)
        pagenew = requests.get(url)
        soup = BeautifulSoup(pagenew.content, 'html.parser')
        #### dealer names
        dealers=[]
        for link in soup.find_all('div', class_="geTextA1", style="padding:10px 10px 10px 0px;"):
            dealers.append(find_between(link.text,"					","				"))
            break
        print(dealers)
        #### website of each dealer, if it exists
        website = []
        for table in soup.find_all('table'):
            if table.text.find("Website")!=-1:
                website.append(find_between(table.text,"Website:\n\n\n","\n\n"))
            break
        print(website)
        #### physical address of each dealer, if it exists
        address=[]
        for table in soup.find_all('table'):
            if table.text.find("Address")!=-1:
                address.append(find_between(table.text,"Address:\n\n\n								","\t\t\t\t\t\t"))
            break
        print(address)
        #### email of each dealer, if it exists
        email=[]
        contacts = []
        for link in soup.find_all('a'):
            contacts.append(link.get('href'))
        for c in contacts:
            if c.find("mailto")!=-1:
                email.append(c[7:]) 
        print(email)
        #### phone number of each dealer, if it exists
        phone = []
        for link in soup.find_all('div', class_="geTextA5"):
            phone.append(find_between(link.text,"								","							"))
            break
        print(phone)

# ------- save data as found, enforce UTF-8 encoding
        data=[]
        if len(dealers)>0: 
            data.append(find_between(dealers[0],'',"\n").encode('utf-8'))
        else:
            data.append("")
        if len(website)>0:
            data.append(website[0].encode('utf-8'))
        else:
            data.append('')
        if len(address)>0:
            data.append(address[0].encode('utf-8'))
        else:
            data.append("")
        if len(email)>0:
            data.append(email[0].encode('utf-8'))
        else:
            data.append("")
        if len(phone)>0:
            data.append(phone[0].encode('utf-8'))
        else:
            data.append("")
        print(data)
        writer.writerow(data)


################################################################
# 3 -------  ending and timing
endtime = datetime.now()

print('------------------')
print('start time = ',start_time)
print('endtime = ', endtime)
print('diff (in seconds) = ', (datetime.now()-start_time).total_seconds())
print('to find data for %s dealers') %len(pages)
print('------------------')

