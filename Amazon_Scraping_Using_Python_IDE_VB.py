import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import bs4
import requests,bs4,lxml,re,csv,datetime,pdb

records=[]

def get_url(url_temp,count):
    URL=url_temp.format(count,count)
    return URL

def extract_records_1(results):
    #item_name=results.find('div','p13n-sc-truncate p13n-sc-line-clamp-2 p13n-sc-truncate-desktop-type2').text.strip()
    item_name=results.a.text.strip()
    item_url='https://www.amazon.in'+results.find('a','a-link-normal').get('href')
    
    try:
        item_price=results.find('span','a-size-base a-color-price').text.replace('\xa0',' ')
    except AttributeError:
        print("There is no price mention") 
        item_price='Item Not Available'
    
    try:
        item_popularity=results.find('span','a-icon-alt').text.replace(' out of 5 stars','')
    except AttributeError:
        print("There is no popularity mention")
        item_popularity='Item Not famous'
        
    return (item_name,item_url,item_price,item_popularity)

def Generate_CSV():
    x = datetime.datetime.now()
    timestamp=x.strftime("%d%m%y%H%M_%f")
    filename='C:\\Users\\sandeshmo\\Downloads\\13-Web-Scraping\\AmazonTodaysDeal_{}.csv'.format(timestamp)
    with open(filename, 'w', newline= '', encoding='utf-8') as f:
        #writer=csv.writer(f, quoting=csv.QUOTE_NONE)
        writer=csv.writer(f)
        writer.writerow(['ITEM NAME ','URL','PRICE ','RAITING '])
        #'''
        try:
            writer.writerows(records)
        except Exception:
            return 'None - Exception occured !!!'
        #'''    
        #writer.writerows(records)


url_temp='https://www.amazon.in/gp/new-releases/boost/ref=zg_bsnr_pg_{}?ie=UTF8&pg={}'
chrome_options = webdriver.ChromeOptions()
#argument to switch off suid sandBox and no sandBox in Chrome 

chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=r'D:\SandeshSadanandMore\Python\Udemy\Chrome Driver\chromedriver.exe', options=chrome_options)

for page in range(1,3):
    response=requests.get(get_url(url_temp,page))
    soup=bs4.BeautifulSoup(response.content,'html.parser')
    results=soup.find_all('li',{'class':'zg-item-immersion'})

    for item in results:
        record=extract_records_1(item)
        if record:
            records.append(record)


Generate_CSV()