import re
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from splinter import Browser
import random
from random import randint
import sys
import logging
import os

__file__ = 'scanner_burkhamer.py'

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

scanner_name = "burkhamer"
vendor_name = "Burkhamer Property Services"
logger.info(scanner_name)
logger.info(vendor_name)
logger.info("------------------------")
path = "https://www.burkhamerpropertyservices.com/available-rental-home-listings"

def assumeBedrooms(bedrooms):
    return 1 if int(bedrooms) == 0 else int(bedrooms)

def cleanCityState(segments):
    if not ',' in segments[-3]:
        segments[-3] = segments[-3] + ","
    if '.' in segments[-2]:
        segments[-2] = segments[-2].replace('.', '')
    return segments

def numbersOnly(text):
    text = text.replace('$','')
    text = text.replace(',','')
    text = text.replace('RENT','')
    text = text.replace('beds', '')
    text = text.replace('bed', '')
    text = text.replace('baths', '')
    text = text.replace('bath', '')
    text = text.replace('s', '')
    text = text.replace('/ Month', '')
    text = text.replace('/mo', '')
    text = text.lstrip()
    text = text.rstrip()
    return text

relative_base_url = path.rsplit('/',1)[0]

browser = Browser('firefox')
browser.visit(path)

for remaining in range(4, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds ...".format(remaining))
    sys.stdout.flush()
    time.sleep(1)
print("\rDone. Moving on ...\n")

page = browser.html
soup = BeautifulSoup(page, "html.parser")

results = soup.find(id="rplSummaryListings")
ras = results.find_all("div", class_="rplSummary")
for ra in ras:
    try:
        # 1 id
        # 2 FirstIngestedOn
        # 3 LastIngestedOn
        strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
        # 4 LocZip
        rplTagl = ra.find("div", class_="rplSummaryTAGL")
        rplTagl = rplTagl.text
        segments = rplTagl.split(" ")
        strLocZip = segments[-1]
        # 5 LocCity
        if not ',' in segments[-3]:
            segments[-3] = segments[-3] + ","
        if '.' in segments[-2]:
            segments[-2] = segments[-2].replace('.', '')
        if segments[-3] == "Shores":
            segments[-3] == "Ocean Shores"
        strLocCity = segments[-3] + " " + segments[-2]
        # 6 LocDesc
        LocDesc = ra.find("div", class_="rplSummaryTAGL")
        strLocDesc = LocDesc.text
        # 7 Price
        strPrice = ra.find("div", class_="rplSummaryRENT")
        strPrice = numbersOnly(strPrice.text)
        # 8 bedrooms
        strBedrooms = ra.find("div", class_="rplSummaryBEDS rplSummarySizeItem")
        strBedrooms = numbersOnly(strBedrooms.text)
        # 9 bathrooms
        strBathrooms = ra.find("div", class_="rplSummaryBATH rplSummarySizeItem")
        strBathrooms = numbersOnly(strBathrooms.text)
        # 10 description
        strDescription = (ra.find("div", class_="rplSummaryREMS")).text
        # 11 url
        strUrl = (ra.find("div", class_="rplSummaryHeaderContent")).get("id")
        # 12 type
        strType = "home"
        # 13 images
        strImages = 1
        # 14 FeaturedImage
        strFeaturedImage = (ra.find("div", class_="rplSummaryThumb")).get("style")
        # 15 PetFriendly
        strPetFriendly = "0"
        # 16 furnished
        strFurnished = "0"
        # 17 CurrentlyAvailable
        strCurrentlyAvailable = "yes"
        # 18 vendor
        strVendor = vendor_name
        # 19 scanner
        strScanner = scanner_name
        # 20 SquareFeet
        strSquareFeet = "0"
        # 21 deposit
        strDeposit = "0"
        # 22 lease
        strLease = "0"

        ## Begin Debug code
        #print(" 1 id: " + strid)
        #print(" 2 FirstIngestedOn: " + strFirstIngestedOn)
        logger.debug(" 3 LastIngestedOn: " + strLastIngestedOn)
        logger.debug(" 4 LocCity: " + strLocCity)
        logger.debug(" 5 LocZip: " + strLocZip)
        logger.debug(" 6 LocDesc: " + strLocDesc)
        logger.debug(" 7 price: " + strPrice)
        logger.debug(" 8 bedrooms: " + strBedrooms)
        logger.debug(" 9 bathrooms: " + strBathrooms)
        logger.debug("10 description: " + strDescription)
        logger.debug("11 url: " + strUrl)
        logger.debug("12 type: " + strType)
        logger.debug("13 images: " + str(strImages))
        logger.debug("14 FeaturedImage: " + strFeaturedImage)
        logger.debug("15 PetFriendly: " + strPetFriendly)
        logger.debug("16 furnished: " + strFurnished)
        logger.debug("17 CurrentlyAvailable: " + strCurrentlyAvailable)
        logger.debug("18 vendor: " + strVendor)
        logger.debug("19 scanner: " + strScanner)
        logger.debug("20 SquareFeet: " + strSquareFeet)
        logger.debug("21 deposit: " + strDeposit)
        logger.debug("22 lease: " + strLease)
        logger.debug("-----------------------------")
    
        # check if exists in db; 
        loc1 = Listing()
        loc1.find_listing_by_url(strUrl)
        if loc1.exists:
            loc1.id_number = loc1.id_number[0]
            loc1.exists = False
            loc1.load_listing(loc1.id_number)
            if loc1.exists:
                logger.info("Listing found.")
                logger.debug(loc1.locDesc)
                logger.debug(loc1.locCity)
                logger.debug(loc1.locZip)
                logger.debug(loc1.price)
                logger.info("Evaluating price update ...")
                if loc1.price != int(strPrice):
                    loc1.set_listing_price(int(strPrice))
                    logger.info("Price should have been updated.")
                logger.info("Evaluating square feet update ...")
                if loc1.squareFeet != int(strSquareFeet):
                    loc1.set_square_feet(int(strSquareFeet))
                loc1.set_currently_available()
                loc1.set_last_ingested(strLastIngestedOn)
        else: 
            logger.info("New listing found, adding to database ...")
            loc1.new_listing(strLastIngestedOn, strLastIngestedOn, strLocZip, strLocCity, strLocDesc, strPrice, strBedrooms, strBathrooms, strDescription, strUrl, strType, 0, strFeaturedImage, 0, 0, "yes", strVendor, strScanner, strSquareFeet, 0, 0)

        logger.info("----------------------------")
    except:
        pass
    
logger.info("Scanning with " + scanner_name + " completed.")
browser.quit()