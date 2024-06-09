import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import logging

__file__ = 'scanner_cathysrentals.py'

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

scanner_name = "cathysrentals"
vendor_name = "Cathy Hinds Home Sweet Home Propery Management"
path = "https://cathyhindspm.appfolio.com/listings?1415168891973#"
logger.info(scanner_name)
logger.info(vendor_name)
logger.info("------------------------")

def assumeBedrooms(bedrooms):
    return 1 if int(bedrooms) == 0 else int(bedrooms)

def numbersOnly(text):
    text = text.replace('$','')
    text = text.replace(',','')
    text = text.replace('RENT','')
    text = text.replace('beds', '')
    text = text.replace('bed', '')
    text = text.replace('bath', '')
    text = text.replace('bd', '')
    text = text.replace('ba', '')
    return text

def cleanCityState(segments):
    if not ',' in segments[-3]:
        segments[-3] = segments[-3] + ","
    if '.' in segments[-2]:
        segments[-2] = segments[-2].replace('.', '')
    for segment in segments:
        segment = segment.rstrip()
        segment = segment.lstrip()
    return segments

relative_base_url = path.rsplit('/',1)[0]
page = requests.get(path)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="result_container")
ras = results.find_all("div", class_="listing-item result js-listing-item")
for ra in ras:
    # 1 id
    # 2 FirstIngestedOn
    # 3 LastIngestedOn
    strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
    # 4 LocZip
    strLocZip = ra.find("span", class_="u-pad-rm js-listing-address")
    strLocZip = strLocZip.text
    segments = strLocZip.split(" ")
    strLocZip = segments[-1]
    # 5 LocCity
    strLocCity = ra.find("span", class_="u-pad-rm js-listing-address")
    strLocCity = strLocCity.text
    segments = strLocCity.split(",")
    segments = cleanCityState(segments)
    strLocCity = segments[-2]
    strLocCity = strLocCity.rstrip()
    strLocCity = strLocCity.lstrip()
    strLocCity = strLocCity + ", WA"
    print(strLocCity)
    # 6 LocDesc
    strLocDesc = ra.find("span", class_="u-pad-rm js-listing-address")
    strLocDesc = strLocDesc.text
    # 7 Price
    #strPrice = ra.find("div", class_="detail-box__item")
    #strPrice = strPrice.find("dd", class_="detail-box__value")
    #strPrice = numbersOnly(strPrice)
    # 7 Price, 8 bedrooms, & 9 bathrooms
    details = ra.find_all("div", class_="detail-box__item")
    strAvailable = "0"
    strBedrooms = "0"
    strBathrooms = "0"
    strPrice = "0"
    for section in details:
        text = section.find("dt")
        if "RENT" in text.text:
            values = section.find("dd")
            strPrice = numbersOnly(values.text)
        if "bath" in text.text.lower():
            values = section.find("dd")
            this = (values.text).split("/")
            strBathrooms = numbersOnly(this[1])
        if "bed" in text.text.lower():
            values = section.find("dd")
            this = (values.text).split("/")
            strBedrooms = numbersOnly(this[0])
        if "available" in text.text.lower():
            values = section.find("dd")
            strAvailable = values.text
    # 10 description
    strDescription = ra.find("span", class_="u-pad-rm js-listing-address")
    if strDescription != None:
        strDescription = strDescription.text
    else:
        strDescription = ""
    # 11 url
    strUrl = ra.find("div", class_="listing-item__figure-container")
    strUrl = strUrl.find("a").get("href")
    # 12 type
    strType = "rental"
    # 13 images
    strImages = 1
    # 14 FeaturedImage
    strFeaturedImage = ra.find("div", class_="listing-item__figure")
    strFeaturedImage = strFeaturedImage.find("img").get("src")
    # 15 PetFriendly
    strPetFriendly = "0"
    # 16 furnished
    strFurnished = "0"
    # 17 CurrentlyAvailable
    strCurrentlyAvailable = strAvailable # this is from section 8 & 9
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
    loc1.find_listing_by_search(strLocDesc, strLocCity, strLocZip)
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
logger.info("Scanning with " + scanner_name + " completed.")