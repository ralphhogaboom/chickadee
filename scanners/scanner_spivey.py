import requests
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import os
import sys
import logger

__file__ = 'scanner_spivey.py'

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

scanner_name = "spivey"
vendor_name = "Spivey Realty Group"
path = "https://rentalsbyspivey.managebuilding.com/Resident/public/rentals?hidenav=true&bedrooms=0&bathrooms=0&location=98520"

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
    return text

relative_base_url = path.rsplit('/',1)[0]
page = requests.get(path)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="rentals-container")
ras = results.find_all("a", class_="featured-listing")
for ra in ras:
    # 1 id
    # 2 FirstIngestedOn
    # 3 LastIngestedOn
    strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
    # 4 LocZip
    cityZip = ra.find("div", class_="featured-listing__description-container")
    LocCity, delimeter, LocZip = (cityZip.p.string).rpartition(" ")
    strLocZip = LocZip.strip()
    # 5 LocCity
    strLocCity = LocCity.strip()
    # 6 LocDesc
    LocDesc = ra.find("img", class_="featured-listing__image")
    strLocDesc = LocDesc.get("alt")
    # 7 Price
    strPrice = ra.get('data-rent')
    # 8 bedrooms
    strBedrooms = str(assumeBedrooms(ra.get('data-bedrooms')))
    # 9 bathrooms
    strBathrooms = ra.get('data-bathrooms')
    # 10 description
    strDescription = (ra.find("p", class_="featured-listing__description").text.strip())
    strDescription = strDescription.join(strDescription.splitlines())
    # 11 url
    strUrl = ra.get('href')
    # 12 type
    strType = ra.get('data-type')
    # 13 images
    # 14 FeaturedImage
    ra_img = ra.find("img", class_="featured-listing__image")
    strFeaturedImage = relative_base_url + "/" + ra_img.get('src')
    # 15 PetFriendly
    # 16 furnished
    # 17 CurrentlyAvailable
    strCurrentlyAvailable = "yes"
    # 18 vendor
    strVendor = vendor_name
    # 19 scanner
    strScanner = scanner_name
    # 20 SquareFeet
    strSquareFeet = ra.get('data-square-feet')
    # 21 deposit
    # 22 lease

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
        #logger.info("Found it with initial search.")
        # logger.info(loc1.id_number[0])
        loc1.id_number = loc1.id_number[0]
        loc1.exists = False
        loc1.load_listing(loc1.id_number)
        if loc1.exists:
            logger.info("Listing found:")
            logger.info(loc1.locDesc)
            logger.info(loc1.locCity)
            logger.info(loc1.locZip)
            logger.info(loc1.price)
            if loc1.price != int(strPrice):
                loc1.set_listing_price(int(strPrice))
            if loc1.squareFeet != int(strSquareFeet):
                loc1.set_square_feet(int(strSquareFeet))
            loc1.set_currently_available()
            loc1.set_last_ingested(strLastIngestedOn)
    else: 
        logger.info("New listing found, adding to database ...")
        loc1.new_listing(strLastIngestedOn, strLastIngestedOn, strLocZip, strLocCity, strLocDesc, strPrice, strBedrooms, strBathrooms, strDescription, strUrl, strType, 0, strFeaturedImage, 0, 0, "yes", strVendor, strScanner, strSquareFeet, 0, 0)

    logger.info("----------------------------")
