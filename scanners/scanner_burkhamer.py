import re
import requests
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
from listing import Listing
from splinter import Browser

scanner_name = "burkhamer"
vendor_name = "Burkhamer Property Services"
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

def taketime():
    time.sleep(round(random.uniform(1.2,9.8),2))

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

        # ## Begin Debug code
        # #print(" 1 id: " + strid)
        # #print(" 2 FirstIngestedOn: " + strFirstIngestedOn)
        # print(" 3 LastIngestedOn: " + strLastIngestedOn)
        # print(" 4 LocCity: " + strLocCity)
        # print(" 5 LocZip: " + strLocZip)
        # print(" 6 LocDesc: " + strLocDesc)
        # print(" 7 price: " + strPrice)
        # print(" 8 bedrooms: " + strBedrooms)
        # print(" 9 bathrooms: " + strBathrooms)
        # print("10 description: " + strDescription)
        # print("11 url: " + strUrl)
        # print("12 type: " + strType)
        # print("13 images: " + str(strImages))
        # print("14 FeaturedImage: " + strFeaturedImage)
        # print("15 PetFriendly: " + strPetFriendly)
        # print("16 furnished: " + strFurnished)
        # print("17 CurrentlyAvailable: " + strCurrentlyAvailable)
        # print("18 vendor: " + strVendor)
        # print("19 scanner: " + strScanner)
        # print("20 SquareFeet: " + strSquareFeet)
        # print("21 deposit: " + strDeposit)
        # print("22 lease: " + strLease)
        # print("-----------------------------")
    

        # check if exists in db; 
        loc1 = Listing()
        loc1.find_listing_by_url(strUrl)
        if loc1.exists:
            loc1.id_number = loc1.id_number[0]
            loc1.exists = False
            loc1.load_listing(loc1.id_number)
            if loc1.exists:
                print("Listing found.")
                # print(loc1.locDesc)
                # print(loc1.locCity)
                # print(loc1.locZip)
                # print(loc1.price)
                print("Evaluating price update ...")
                if loc1.price != int(strPrice):
                    loc1.set_listing_price(int(strPrice))
                    print("Price should have been updated.")
                print("Evaluating square feet update ...")
                if loc1.squareFeet != int(strSquareFeet):
                    loc1.set_square_feet(int(strSquareFeet))
                loc1.set_currently_available()
                loc1.set_last_ingested(strLastIngestedOn)
        else: 
            print("New listing found, adding to database ...")
            loc1.new_listing(strLastIngestedOn, strLastIngestedOn, strLocZip, strLocCity, strLocDesc, strPrice, strBedrooms, strBathrooms, strDescription, strUrl, strType, 0, strFeaturedImage, 0, 0, "yes", strVendor, strScanner, strSquareFeet, 0, 0)

        print("----------------------------")
    except:
        pass
    
browser.quit()