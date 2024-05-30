import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import sys
sys.path.append("C:\\Users\\ralph\\Documents\\Antsy Chickadee")
from listing import Listing

scanner_name = "cathysrentals"
vendor_name = "Cathy Hinds Home Sweet Home Propery Management"

# path = "http://ralph.hogaboom.org/chickadee/cathysrentals/cathysrentals.htm"
path = "https://cathyhindspm.appfolio.com/listings?1415168891973#"

relative_base_url = path.rsplit('/',1)[0]
page = requests.get(path)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="result_container")

def numbersOnly(text):
    pattern = r'\d+'
    text.replace('$','')
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return 0
    
def cleanCityState(segments):
    if not ',' in segments[-3]:
        segments[-3] = segments[-3] + ","
    if '.' in segments[-2]:
        segments[-2] = segments[-2].replace('.', '')
    return segments

# ras == rental attributes
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
    segments = strLocCity.split(" ")
    segments = cleanCityState(segments)
    strLocCity = segments[-3] + " " + segments[-2]
    # 6 LocDesc
    strLocDesc = ra.find("span", class_="u-pad-rm js-listing-address")
    strLocDesc = strLocDesc.text
    # 7 Price
    strPrice = ra.find("div", class_="detail-box__item")
    strPrice = strPrice.find("dd", class_="detail-box__value")
    # 8 bedrooms & 9 bathrooms
    details = ra.find_all("div", class_="detail-box__item")
    strBedrooms = ""
    strBathrooms = ""
    strPrice = ""
    strAvailable = ""
    for section in details:
        text = section.find("dt")
        if "RENT" in text.text:
            values = section.find("dd")
            strPrice = values.text
        if "bath" in text.text.lower():
            values = section.find("dd")
            this = (values.text).split("/")
            strBathrooms = this[1]
        if "bed" in text.text.lower():
            values = section.find("dd")
            this = (values.text).split("/")
            strBedrooms = this[0]
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
 