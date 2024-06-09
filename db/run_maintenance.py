import sys
import os
import logging

__file__ = 'run_maintenance.py'

libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, libdir)
from class_listing import Listing

listing = Listing()

# get all the id's where the zip is empty.
listing.find_all_empty_zips()
for row in listing.results:
    thisZip = row[1].lower()
    if "aberdeen" in thisZip:
        listing.update_zip(row[0], "98520")
    if "amanda park" in thisZip:
        listing.update_zip(row[0], "98526")
    if "copalis" in thisZip:
        listing.update_zip(row[0], "98536")
    if "copalis beach" in thisZip:
        listing.update_zip(row[0], "98535")
    if "cosmopolis" in thisZip:
        listing.update_zip(row[0], "98537")
    if "elma" in thisZip:
        listing.update_zip(row[0], "98541")
    if "grayland" in thisZip:
        listing.update_zip(row[0], "98547")
    if "hoquiam" in thisZip:
        listing.update_zip(row[0], "98550")
    if "humptulips" in thisZip:
        listing.update_zip(row[0], "98552")
    if "mccleary" in thisZip:
        listing.update_zip(row[0], "98557")
    if "malone" in thisZip:
        listing.update_zip(row[0], "98559")
    if "moclips" in thisZip:
        listing.update_zip(row[0], "98562")
    if "montesano" in thisZip:
        listing.update_zip(row[0], "98563")
    if "neilton" in thisZip:
        listing.update_zip(row[0], "98566")
    if "oakville" in thisZip:
        listing.update_zip(row[0], "98568")
    if "ocean shores" in thisZip:
        listing.update_zip(row[0], "98569")
    if "pacific beach" in thisZip:
        listing.update_zip(row[0], "98571")
    if "quinault" in thisZip:
        listing.update_zip(row[0], "98575")
    if "satsop" in thisZip:
        listing.update_zip(row[0], "98583")
    if "tahola" in thisZip:
        listing.update_zip(row[0], "98578")
    if "westport" in thisZip:
        listing.update_zip(row[0], "98595")
    if "raymond" in thisZip:
        listing.update_zip(row[0], "98577")
    if "south bend" in thisZip:
        listing.update_zip(row[0], "98586")

logger.info("Now running updates on availability.")

listing.update_available()

logger.info("Availability update completed.")

listing.update_days_on_market()















