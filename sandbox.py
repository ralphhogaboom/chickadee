import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from listing import Listing

scanner_name = "cathysrentals"
vendor_name = "Cathy Hinds Home Sweet Home Propery Management"
path = "https://cathyhindspm.appfolio.com/listings?1415168891973#"

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
