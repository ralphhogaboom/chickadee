import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import sys
sys.path.append("C:\\Users\\ralph\\Documents\\Antsy Chickadee")
from listing import Listing

scanner_name = "ssrealty"
vendor_name = "South Shore Realty"
path = "https://ralph.hogaboom.org/chickadee/ssrealty.htm"

def assumeBedrooms(bedrooms):
    return 1 if int(bedrooms) == 0 else int(bedrooms)

def numbersOnly(text):
    text = text.replace('$','')
    text = text.replace(',','')
    text = text.replace('RENT','')
    text = text.replace('beds', '')
    text = text.replace('bed', '')
    text = text.replace('bath', '')
    return text

def cleanCityState(segments):
    if not ',' in segments[-3]:
        segments[-3] = segments[-3] + ","
    if '.' in segments[-2]:
        segments[-2] = segments[-2].replace('.', '')
    return segments

relative_base_url = path.rsplit('/',1)[0]
page = requests.get(path)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="1903639482")
ras = results.find_all("div", class_="listing-item")
for ra in ras:
    # 1 id
    # 2 FirstIngestedOn
    # 3 LastIngestedOn
    strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
    # 4 LocZip
    strAddress = ra.find("h2", class_="address")
    strAddress = strAddress.text
    segments = strAddress.split(" ")
    strLocZip = segments[-1]
    # 5 LocCity
    strAddress = ra.find("h2", class_="address")
    strAddress = strAddress.text
    segments = strAddress.split(" ")
    segments = cleanCityState(segments)
    strLocCity = segments[-3] + " " + segments[-2]
    # 6 LocDesc
    strLocDesc = ra.find("div", class_="tagline")
    strLocDesc = strLocDesc.text
    # 7 Price
    strPrice = ra.find("h3", class_="rent")
    strPrice = numbersOnly(strPrice.text)
    # 8 bedrooms
    strBedrooms = ra.find("div", class_="feature beds")
    strBedrooms = numbersOnly(strBedrooms.text)
    # 9 bathrooms
    strBathrooms = ra.find("div", class_="feature baths")
    strBathrooms = numbersOnly(strBathrooms.text)
    # 10 description
    strDescription = ra.find("h2", class_="address")
    strDescription = strDescription.text
    # 11 url
    strUrl = (ra.find("a", class_="slider-link")).get("href")
    # 12 type
    strType = "home"
    # 13 images
    strImages = 1
    # 14 FeaturedImage
    strFeaturedImage = (ra.find("div", class_="slider-image")).get("data-background-image")
    # 15 PetFriendly
    strPetFriendly = "0"
    # 16 furnished
    strFurnished = "0"
    # 17 CurrentlyAvailable
    strAvailable = (ra.find("div", class_="available")).text
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

    """ ## Begin Debug code
    #print(" 1 id: " + strid)
    #print(" 2 FirstIngestedOn: " + strFirstIngestedOn)
    print(" 3 LastIngestedOn: " + strLastIngestedOn)
    print(" 4 LocCity: " + strLocCity)
    print(" 5 LocZip: " + strLocZip)
    print(" 6 LocDesc: " + strLocDesc)
    print(" 7 price: " + strPrice)
    print(" 8 bedrooms: " + strBedrooms)
    print(" 9 bathrooms: " + strBathrooms)
    print("10 description: " + strDescription)
    print("11 url: " + strUrl)
    print("12 type: " + strType)
    print("13 images: " + str(strImages))
    print("14 FeaturedImage: " + strFeaturedImage)
    print("15 PetFriendly: " + strPetFriendly)
    print("16 furnished: " + strFurnished)
    print("17 CurrentlyAvailable: " + strCurrentlyAvailable)
    print("18 vendor: " + strVendor)
    print("19 scanner: " + strScanner)
    print("20 SquareFeet: " + strSquareFeet)
    print("21 deposit: " + strDeposit)
    print("22 lease: " + strLease)
    print("-----------------------------")
    """

    # check if exists in db; 
    loc1 = Listing()
    loc1.find_listing_by_search(strLocDesc, strLocCity, strLocZip)
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
 