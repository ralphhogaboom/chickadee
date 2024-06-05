import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from listing import Listing
import time
import random

from splinter import Browser
import pandas as pd
import matplotlib.pyplot as plt
import time

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
    text = text.lstrip()
    text = text.rstrip()
    return text

def taketime():
    time.sleep(round(random.uniform(1.2,9.8),2))

parentBrowser = Browser('firefox')
base_url = "https://www.facebook.com/marketplace/114113988602319/propertyrentals/?"
base_url = "https://www.facebook.com/marketplace/104028649634847/propertyrentals/?"

scanner_name = "facebook_corvallis"
vendor_name = "Facebook Marketplace"

lat = 47.1187
lat = (round(random.uniform(46.834,47.0541),4))
long = -123.7706
long = (round(random.uniform(-124.1017,-123.6774),4))
radius = (round(random.uniform(15,35),0))
exact = "false"

# url = f"{base_url|}minBathrooms={minBathrooms}&minBedrooms={minBedrooms}&propertyType={propertyType}&exact={exact}"
starturl = f"{base_url}latitude={lat}&longitude={long}&radius={radius}&exact={exact}"
starturl = f"{base_url}"

parentBrowser.visit(starturl)

page = parentBrowser.html
soup = BeautifulSoup(page, "html.parser")

i = 0
strUrl = ""

ras = soup.find_all("div", class_="x3ct3a4")
for ra in ras:
    i = i + 1
    value = ra.find("a", class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv").get("href")
    # print("URL: " + strUrl)
    # details = ra.find("img", class_="xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3").get("alt")
    # strFeaturedImage = ra.find("img", class_="xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3").get("src")
    # print("Featured Image: " + strFeaturedImage)
    # print("Listing " + str(i) + " details: "  + details)
    # print("000000000000000000000000000000000000000000000000000")
    strUrl = strUrl + value + ","

urls = tuple(strUrl.split(','))

for url in urls:
    listing_url = "https://www.facebook.com" + url
    taketime()
    browser = Browser('firefox')
    browser.visit(listing_url)
    listing_page = browser.html
    listing_soup = BeautifulSoup(listing_page, "html.parser")

    try:
        # zero out the unreliable variables
        strBedrooms = "0"
        strBathrooms = "0"
        strLocCity = "0"
        strType = "rental"
        strPetFriendly = "0"
        strFurnished = "0"
        strCurrentlyAvailable = "now"
        strLease = "0"
        # 1 id
        # 2 FirstIngestedOn
        # 3 LastIngestedOn
        strLastIngestedOn = datetime.today().strftime('%Y-%m-%d')
        # 4 LocZip
        strLocZip = "" # Page doesn't provide a zip; will need a later lookup to backfill the database.
        # 6 LocDesc
        strLocDesc = "0"
        snippet = listing_soup.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u")
        strLocDesc = snippet.text
        print("strLocDesc: " + strLocDesc)
        # 5 LocCity
        snippet = listing_soup.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "," in chunk.text:
                strLocCity = chunk.text
                strLocCity = strLocCity.split(',')
                print("strLocCity: ")
                print(strLocCity)
                strLocCity = strLocCity[-2] + ", " + strLocCity[-1]
                strLocCity = strLocCity.lstrip()
                strLocCity = strLocCity.rstrip()
                print("strLocCity: ")
                print(strLocCity)
        # 7 Price
        strPrice = listing_soup.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
        strPrice = numbersOnly(strPrice.text)
        # 8 bedrooms & 9 bathrooms
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for aRoom in snippet:
            if " · " in aRoom.text:
                value = aRoom.text
                value = value.split(" · ")
                strBedrooms = numbersOnly(value[0])
                strBathrooms = numbersOnly(value[1])
        # 10 description
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")
        for desc in snippet:
            if "..." in desc.text:
                strDescription = desc.text
        # 11 url
        strUrl = listing_url.split("?")
        strUrl = strUrl[0]
        # 12 type
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "apartment" in (chunk.text).lower():
                strType = chunk.text
            elif "house" in (chunk.text).lower():
                strType = chunk.text
        # 13 images
        strImages = 1
        # 14 FeaturedImage
        strFeaturedImage = listing_soup.find("img", class_="xz74otr").get("src")
        # 15 PetFriendly
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "dog" in (chunk.text).lower():
                strPetFriendly = chunk.text
            if "cat" in (chunk.text).lower():
                strPetFriendly = chunk.text
        # 16 furnished
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "urnished" in chunk.text:
                strFurnished = chunk.text
        # 17 CurrentlyAvailable
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "available now" in (chunk.text).lower():
                strCurrentlyAvailable = chunk.text
        # 18 vendor
        strVendor = vendor_name
        # 19 scanner
        strScanner = scanner_name
        # 20 SquareFeet
        strSquareFeet = "0"
        # 21 deposit
        strDeposit = "0"
        # 22 lease
        snippet = listing_soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        for chunk in snippet:
            if "lease" in (chunk.text).lower():
                strLease = chunk.text

        # check if exists in db; 
        listing = Listing()
        print(strUrl)
        listing.find_listing_by_url(str(strUrl))
        if listing.exists:
            listing.id_number = listing.id_number[0]
            listing.exists = False
            listing.load_listing(listing.id_number)
            if listing.exists:
                print("Listing found.")
                print("Evaluating price update ...")
                if listing.price != int(strPrice):
                    listing.set_listing_price(int(strPrice))
                    print("Price should have been updated.")
                print("Evaluating square feet update ...")
                if listing.squareFeet != int(strSquareFeet):
                    listing.set_square_feet(int(strSquareFeet))
                listing.set_currently_available()
                listing.set_last_ingested(strLastIngestedOn)
        else: 
            print("New listing found, adding to database ...")
            listing.new_listing(strLastIngestedOn, strLastIngestedOn, strLocZip, strLocCity, strLocDesc, strPrice, strBedrooms, strBathrooms, strDescription, strUrl, strType, 0, strFeaturedImage, 0, 0, "yes", strVendor, strScanner, strSquareFeet, 0, 0)

        print("----------------------------")
        browser.quit()
    except:
        browser.quit()
        pass
print("Total listings found: " + str(i))

parentBrowser.quit()

