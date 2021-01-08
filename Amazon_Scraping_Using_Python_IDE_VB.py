           


import csv
from selenium import webdriver   # If you want to access link using webdriver but we are using normal "requests" libs to achive our motto.
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import bs4

import requests,bs4,lxml,re,csv,datetime,pdb   # imported during debugging the code.

#list to add records in format of tuples
records=[]   

#important link to access the site.
url_temp='https://www.amazon.in/gp/new-releases/boost/ref=zg_bsnr_pg_{}?ie=UTF8&pg={}'   ## Link to access top Amazon Launchpad products.


#URL forming function
def get_url(url_temp,count): 
    URL=url_temp.format(count,count)
    return URL


#extracting records from response
def extract_records_1(results):
    #item_name=results.find('div','p13n-sc-truncate p13n-sc-line-clamp-2 p13n-sc-truncate-desktop-type2').text.strip()
    item_name=results.a.text.strip()
    item_url='https://www.amazon.in'+results.find('a','a-link-normal').get('href')
    
    #Handling if attribute is not available in response.
    try:
        item_price=results.find('span','a-size-base a-color-price').text.replace('\xa0',' ')
    except AttributeError:
        print("There is no price mention") 
        item_price='Item Not Available'
        
    #Handling if attribute is not available in response.
    try:
        item_popularity=results.find('span','a-icon-alt').text.replace(' out of 5 stars','')
    except AttributeError:
        print("There is no popularity mention")
        item_popularity='Item Not famous'
        
    return (item_name,item_url,item_price,item_popularity)    # Returning single tuple with name , URL, price and popularity



#Get the data into csv file which has been extracted in form of tuple.
def Generate_CSV():
    x = datetime.datetime.now()
    timestamp=x.strftime("%d%m%y%H%M_%f")
    filename='C:\\Users\\<YourUserName>\\Downloads\\Web-Scraping\\AmazonTodaysDeal_{}.csv'.format(timestamp)
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


'''

chrome_options = webdriver.ChromeOptions()      # To pass arguments during accessing chrome driver
#argument to switch off suid sandBox and no sandBox in Chrome 

chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=r'D:\SanMore\Python\Udemy\Chrome Driver\chromedriver.exe', options=chrome_options)

'''

#Extracting data into "records: list.

for page in range(1,3):   # Actually only 2 pages data is available on Amazon website. so range is 1 & 2 only. i.e. range(1,3)  
    response=requests.get(get_url(url_temp,page))
    soup=bs4.BeautifulSoup(response.content,'html.parser')  ## Getting response and giving command to Beautiyful-soup to parse it into html format.
    results=soup.find_all('li',{'class':'zg-item-immersion'})  # Reading class tag with class name "zg-item-immersion"

# 
    for item in results:
        record=extract_records_1(item)
        if record:
            records.append(record)


# Calling CSV function
Generate_CSV()
