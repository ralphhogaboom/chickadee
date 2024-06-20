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

debug = True
scanner_name = "burkhamer"
vendor_name = "Burkhamer Property Services"
print("[burkhamer] ",scanner_name)
print("[burkhamer] ",vendor_name)
print("[burkhamer] ","------------------------")
path = "https://www.burkhamerpropertyservices.com/available-rental-home-listings"
browser = Browser('firefox')
browser.visit(path)

relative_base_url = path.rsplit('/',1)[0]

for remaining in range(4, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds ...".format(remaining))
    sys.stdout.flush()
    time.sleep(1)
sys.stdout.write("Done. Moving on ...\n")

page = browser.html
soup = BeautifulSoup(page, "html.parser")

listing = Listing()

results = soup.find(id="rplSummaryListings")
ras = results.find_all("div", class_="rplSummary")
for ra in ras:
    # find the unique tag
    try:
        strUniqueValue = (ra.find("div", class_="rplSummaryHeaderContent")).get("id")
    except:
        strUniqueValue = ""
    if len(strUniqueValue) != 0:
        if listing.searchUnique(strUniqueValue) == 0:
            listing.createNew(strUniqueValue)
            listing.searchUnique(strUniqueValue)
        else:
            if debug: print("[burkhamer] ","Existing location found:")
        if debug: print("[burkhamer] ","ID: ", listing.id_number)
        if listing.exists == False:
            listing.createNew(strUniqueValue)
            listing.searchUnique(strUniqueValue)
        # Run updates.
        if debug: print("[burkhamer] ", "Updating ...")

        # 3 LastIngestedOn
        strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
        listing.setLastIngestedOn(listing.id_number, strLastIngestedOn)

        # 4 LocZip
        rplTagl = ra.find("div", class_="rplSummaryTAGL")
        rplTagl = rplTagl.text
        segments = rplTagl.split(" ")
        strLocZip = segments[-1]
        listing.setLocZip(listing.id_number, strLocZip)

        # 5 LocCity
        if not ',' in segments[-3]:
            segments[-3] = segments[-3] + ","
        if '.' in segments[-2]:
            segments[-2] = segments[-2].replace('.', '')
        if segments[-3] == "Shores":
            segments[-3] == "Ocean Shores"
        strLocCity = segments[-3] + " " + segments[-2]
        listing.setLocCity(listing.id_number, strLocCity)

        # 6 LocDesc
        LocDesc = ra.find("div", class_="rplSummaryTAGL")
        strLocDesc = LocDesc.text
        listing.setLocDesc(listing.id_number, strLocDesc)

        # 7 Price
        strPrice = ra.find("div", class_="rplSummaryRENT")
        strPrice = numbersOnly(strPrice.text)
        listing.setPrice(listing.id_number, strPrice)

        # 8 bedrooms
        strBedrooms = ra.find("div", class_="rplSummaryBEDS rplSummarySizeItem")
        strBedrooms = numbersOnly(strBedrooms.text)
        listing.setBedrooms(listing.id_number, strBedrooms)

        # 9 bathrooms
        strBathrooms = ra.find("div", class_="rplSummaryBATH rplSummarySizeItem")
        strBathrooms = numbersOnly(strBathrooms.text)
        listing.setBathrooms(listing.id_number, strBathrooms)

        # 10 description
        strDescription = (ra.find("div", class_="rplSummaryREMS")).text
        listing.setDescription(listing.id_number, strDescription)

        # 11 url
        strUrl = (ra.find("div", class_="rplSummaryHeaderContent")).get("id")
        listing.setUrl(listing.id_number, strUrl)

        # 12 type
        try:
            strType = (ra.find("img", class_="icon24_1")).get("title")
            listing.setType(listing.id_number, strType)
        except:
            strType = "rental"

        # 13 images
        strImages = 1
        listing.setImages(listing.id_number, strImages)
        
        # 14 FeaturedImage
        try:
            shortVal = strUniqueValue.replace("rplSummaryHeaderContentWA", "")
            shortVal = ("rplSummaryPhotoWA" + shortVal)
            photo_div = soup.find("div", id=shortVal)
            style = photo_div['style']
            url_match = re.search(r'url\((.*?)\)', style)
            if url_match:
                image_url = url_match.group(1).strip('\'"')
                image_url = "https:" + image_url
                print(image_url)
                listing.setFeaturedImage(listing.id_number, image_url)
            else:
                print("URL not found")
            print("------------------------")
        except:
            pass


        # 15 PetFriendly
        strPetFriendly = "0"
        listing.setPetFriendly(listing.id_number, strPetFriendly)

        # 16 furnished
        strFurnished = "0"
        listing.setFurnished(listing.id_number, strFurnished)

        # 17 CurrentlyAvailable
        strCurrentlyAvailable = "yes"
        listing.setCurrentlyAvailable(listing.id_number, strCurrentlyAvailable)

        # 18 vendor
        strVendor = vendor_name
        listing.setVendor(listing.id_number, strVendor)

        # 19 scanner
        strScanner = scanner_name
        listing.setScanner(listing.id_number, strScanner)

        # 20 SquareFeet
        strSquareFeet = "0"
        listing.setSquareFeet(listing.id_number, strSquareFeet)

        # 21 deposit
        strDeposit = "0"
        listing.setDeposit(listing.id_number, strDeposit)

        # 22 lease
        strLease = "0"
        listing.setLease(listing.id_number, strLease)

    else:
        if debug: print("[burkhamer] ","Empty div found, skipping ...")
        # ## Begin Debug code
        # #print(" 1 id: " + strid)
        # #print(" 2 FirstIngestedOn: " + strFirstIngestedOn)
        # if debug: print("[burkhamer] 3 LastIngestedOn: " + strLastIngestedOn)
        # if debug: print("[burkhamer] 4 LocCity: " + strLocCity)
        # if debug: print("[burkhamer] 5 LocZip: " + strLocZip)
        # if debug: print("[burkhamer] 6 LocDesc: " + strLocDesc)
        # if debug: print("[burkhamer] 7 price: " + strPrice)
        # if debug: print("[burkhamer] 8 bedrooms: " + strBedrooms)
        # if debug: print("[burkhamer] 9 bathrooms: " + strBathrooms)
        # if debug: print("[burkhamer] 10 description: " + strDescription)
        # if debug: print("[burkhamer] 11 url: " + strUrl)
        # if debug: print("[burkhamer] 12 type: " + strType)
        # if debug: print("[burkhamer] 13 images: " + str(strImages))
        # if debug: print("[burkhamer] 14 FeaturedImage: " + strFeaturedImage)
        # if debug: print("[burkhamer] 15 PetFriendly: " + strPetFriendly)
        # if debug: print("[burkhamer] 16 furnished: " + strFurnished)
        # if debug: print("[burkhamer] 17 CurrentlyAvailable: " + strCurrentlyAvailable)
        # if debug: print("[burkhamer] 18 vendor: " + strVendor)
        # if debug: print("[burkhamer] 19 scanner: " + strScanner)
        # if debug: print("[burkhamer] 20 SquareFeet: " + strSquareFeet)
        # if debug: print("[burkhamer] 21 deposit: " + strDeposit)
        # if debug: print("[burkhamer] 22 lease: " + strLease)
        if debug: print("[burkhamer] -----------------------------")

if debug: print("[burkhamer] ","Scanning with " + scanner_name + " completed.")
browser.quit()