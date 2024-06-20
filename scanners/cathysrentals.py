import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys

debug = True

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

scanner_name = "cathysrentals"
vendor_name = "Cathy Hinds Home Sweet Home Propery Management"
path = "https://cathyhindspm.appfolio.com/listings?1415168891973#"
if debug: print("[cathysrentals] ",scanner_name)
if debug: print("[cathysrentals] ",vendor_name)
if debug: print("[cathysrentals] ","------------------------")

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

listing = Listing()

results = soup.find(id="result_container")
nodes = results.find_all("div", class_="listing-item result js-listing-item")
for node in nodes:
    # Find the unique value
    try:
        strUniqueValue = node.find("div", class_="listing-item__figure-container")
        strUniqueValue = strUniqueValue.find("a").get("href")
    except:
        strUniqueValue = ""
    if len(strUniqueValue) != 0:
        if listing.searchUnique(strUniqueValue) == 0:
            listing.createNew(strUniqueValue)
            listing.searchUnique(strUniqueValue)
        else:
            if debug: print("[cathys] ","Existing location found:")
        if debug: print("[cathys] ","ID: ", listing.id_number)
        if listing.exists == False:
            listing.createNew(strUniqueValue)
            listing.searchUnique(strUniqueValue)
        # Run updates.
        if debug: print("[cathys] ", "Updating ...")

        # 3 LastIngestedOn
        strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
        listing.setLastIngestedOn(listing.id_number, strLastIngestedOn)        

        # 4 LocZip
        strLocZip = node.find("span", class_="u-pad-rm js-listing-address")
        strLocZip = strLocZip.text
        segments = strLocZip.split(" ")
        strLocZip = segments[-1]
        listing.setLocZip(listing.id_number, strLocZip)

        # 5 LocCity
        strLocCity = node.find("span", class_="u-pad-rm js-listing-address")
        strLocCity = strLocCity.text
        segments = strLocCity.split(",")
        segments = cleanCityState(segments)
        strLocCity = segments[-2]
        strLocCity = strLocCity.rstrip()
        strLocCity = strLocCity.lstrip()
        strLocCity = strLocCity + ", WA"
        listing.setLocCity(listing.id_number, strLocCity)

        # 6 LocDesc
        strLocDesc = node.find("span", class_="u-pad-rm js-listing-address")
        strLocDesc = strLocDesc.text
        listing.setLocDesc(listing.id_number, strLocDesc)

        # 7 Price, 8 bedrooms, & 9 bathrooms
        details = node.find_all("div", class_="detail-box__item")
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
            if "available" in text.text.lower(): #we just parking this for later
                values = section.find("dd")
                strCurrentlyAvailable = values.text
        listing.setPrice(listing.id_number, strPrice)
        listing.setBedrooms(listing.id_number, strBedrooms)
        listing.setBathrooms(listing.id_number, strBathrooms)

        # 10 description
        strDescription = node.find("span", class_="u-pad-rm js-listing-address")
        if strDescription != None:
            strDescription = strDescription.text
        else:
            strDescription = ""
        listing.setDescription(listing.id_number, strDescription)

        # 11 url
        strUrl = node.find("div", class_="listing-item__figure-container")
        strUrl = strUrl.find("a").get("href")
        listing.setUrl(listing.id_number, strUrl)

        # 12 type
        strType = "rental"
        listing.setType(listing.id_number, strType)

        # 14 FeaturedImage
        strFeaturedImage = node.find("div", class_="listing-item__figure")
        strFeaturedImage = strFeaturedImage.find("img").get("src")
        listing.setFeaturedImage(listing.id_number, strFeaturedImage)

        # 13 images
        if strFeaturedImage:
            strImages = 1
            listing.setImages(listing.id_number, strImages)

        # 15 PetFriendly
        if node.find("span", class_="js-listing-pet-policy"):
            strPetFriendly = node.find("span", class_="js-listing-pet-policy").text
        else:
            strPetFriendly = "0"
        listing.setPetFriendly(listing.id_number, strPetFriendly)

        # 16 furnished
        try:
            strFurnished = (node.find("h2", class_="listing-item__title js-listing-title")).text
            if (strFurnished.lower()).find("furnished"): 
                (strFurnished.lower()).find("furnished")
            else:
                strFurnished = "0"
            listing.setFurnished(listing.id_number, strFurnished)
        except:
            pass

        # 17 CurrentlyAvailable, we have this from section 8 & 9
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


    if debug: print("[cathysrentals] ","----------------------------")
if debug: print("[cathysrentals] ","Scanning with " + scanner_name + " completed.")