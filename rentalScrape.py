#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import subprocess

def get_table(building_name, url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find('table')
    df=pd.read_html(str(table))[0]
    today = str(datetime.datetime.now())
    df['date']=today
    df['building']=building_name
    df['url'] = url
    return df

def get_buildings():
    url = "https://appliedapartments.com/properties-apartments-for-rent/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    #soup = BeautifulSoup(result.text, "lxml")
    soup = BeautifulSoup(result.text, "html.parser")

    building_names = []
    for a in soup.select('h2'):
        building_names.append(a.text)

    building_urls = []
    for b in soup.select('a[href*="https://appliedapartments.com/buildings/"]'):
        building_urls.append(b['href'])

    building_list = dict(zip(building_names,building_urls))
    return building_list

buildings=get_buildings()

df=pd.DataFrame()
for building_name,url in buildings.items():
    print(building_name + ": " + url)
    try:
        df=df.append(get_table(building_name,url), ignore_index=True)
    except:
        print("No apartments found in: "+building_name)
        continue

#today = datetime.date.today()
today_now = str(datetime.datetime.now()).replace(" ","_")
filename=(today_now+'.csv')

# adding a filter based on bedroom
#df = df.query('Bedrooms>=3')
#df = df[df.Bedrooms == '3']

print("Results stored in: "+filename)
df.to_csv(filename)

#commandline='echo "Rental Scrape Raw Data" | mail -s "Rental Scrape Raw Data" <youremail> -A '+filename
#print(commandline)
#subprocess.Popen(commandline, shell=True)
