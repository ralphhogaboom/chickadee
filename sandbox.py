import re
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from splinter import Browser
import random
from random import randint
import sys
import os
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

debug = True
scanner_name = "burkhamer"
vendor_name = "Burkhamer Property Services"
path = "https://www.burkhamerpropertyservices.com/available-rental-home-listings"
browser = Browser('firefox')
browser.visit(path)
time.sleep(2)

relative_base_url = path.rsplit('/',1)[0]
page = browser.html
soup = BeautifulSoup(page, "html.parser")


results = soup.find(id="rplSummaryListings")
nodes = results.find_all("div", class_="rplSummary")
for node in nodes:
    try:
        strUniqueValue = (node.find("div", class_="rplSummaryHeaderContent")).get("id")
        shortVal = strUniqueValue.replace("rplSummaryHeaderContentWA", "")
        shortVal = ("rplSummaryPhotoWA" + shortVal)
        print(shortVal)
        print("~~~")
        print(node['style'])
        print("------------------")
    except:
        pass
browser.quit()