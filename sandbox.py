import requests
from datetime import datetime
from bs4 import BeautifulSoup
from listing import Listing

scanner_name = "burkhamer"
vendor_name = "Burkhamer Property Services"

path = "http://ralph.hogaboom.org/chickadee/cathysrentals/cathysrentals.htm"
relative_base_url = path.rsplit('/',1)[0]
page = requests.get(path)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="result_container")

def cleanCityState(segments):
    if not ',' in segments[-3]:
        segments[-3] = segments[-3] + ","
    if '.' in segments[-2]:
        segments[-2] = segments[-2].replace('.', '')
    return segments

# def numbersOnly(text):
#     pattern = r'\d+'
#     text.replace('$','')
#     match = re.search(pattern, text)
#     if match:
#         return match.group()
#     else:
#         return 0

# ras == rental attributes
ras = results.find_all("div", class_="listing-item result js-listing-item")
for ra in ras:
    strLocCity = ra.find("span", class_="u-pad-rm js-listing-address")
    strLocCity = strLocCity.text

    segments = strLocCity.split(" ")
    segments = cleanCityState(segments)
    strLocCity = segments[-3] + " " + segments[-2]
    print(strLocCity)
