###############################################################################

# Parsing RSI Website

###############################################################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

###############################################################################

# build path & build directory to save file from request.get results
__dir__ = os.path.dirname(os.path.realpath('__file__'))
dir_res = os.path.join(__dir__,'data')
try :
    os.mkdir(dir_res)
except FileExistsError :
    print("Directory already exist")

###############################################################################

# Get SC Ship page and scroll to the bottom to get all ships loaded
URL = "https://robertsspaceindustries.com/pledge/ships"

driver = webdriver.Firefox(executable_path="./files/webdrivers/geckodriver")
driver.get(URL)

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)
driver.close()


###############################################################################

# Read the driver page with beautifulsoup
soup = BeautifulSoup(driver.page_source)

#with open("data/Ships_pages_manual.html", 'rb') as fp:
#    soup = BeautifulSoup(fp, 'html.parser')

# Get the list of ships
ShipsList = soup.find('ul', attrs={'class':'ships-listing'}).find_all("li")

ShipsList[0]

list_ships = []

for item in ShipsList :

    tmp = item.find("span", {"class": "name trans-02s"}).get_text()
    
    print(tmp)

    if(len(tmp.split('-')) > 2) :
        name = ' '.join(tmp.split('-')[0:(len(tmp.split('-'))-1)])
        role = tmp.split('-')[len(tmp.split('-'))-1]
    else :
        name = tmp.split('-')[0]
        role = tmp.split('-')[1]
    
    url = "https://robertsspaceindustries.com"+ item.find("a", {"class": "gradient trans-02s"})['href']
    list_ships = list_ships + [[name, role, url]]

print(list_ships)

###############################################################################

# Convert list of list to dataframe

df = pd.DataFrame(list_ships)
df