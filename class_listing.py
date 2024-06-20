import pathlib
import sqlite3
from sqlite3 import Error
from datetime import datetime

debug = True

global db
db = pathlib.Path(__file__).parent.resolve() / "db/db.sqlite3"

print(db)

connection = sqlite3.connect(db)
cursor = connection.cursor()

if debug: connection.set_trace_callback(print)

class Listing:
    def __init__(self, id_number=-1):
        if debug: print("[listing] ", "Starting log ...")
        self.id_number = id
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def createNew(self, unique):
        strNow = datetime.today().strftime('%Y-%m-%d')
        values = unique, strNow, strNow
        cursor.execute("""
        INSERT INTO rentals (uniqueValue, firstIngestedOn, lastIngestedOn) VALUES (?, ?, ?);
        """, values)
        connection.commit()
        if debug: print("[listing] ", "New listing successfully added.")

    def searchUnique(self, unique):
        if debug: print("[listing] ","findByUnique (type): ", type(unique))
        if debug: print("[listing] ","findByUnique (value): ", unique)
        values = (unique,)
        cursor.execute("""
        SELECT id FROM rentals WHERE uniqueValue = ?;
        """, values)
        results = cursor.fetchone()
        if results:
            if debug: print("[listing] ","A result was found")
            self.exists = True
            self.id_number = results[0]
            if debug: print("[listing] ",type(self.id_number))
        else:
            if debug: print("[listing] ","No result found for query with values")
            if debug: print("[listing] ",values[0])
            self.id_number = ""
            self.exists = False
            return 0

    def setLastIngestedOn(self, unique, lastIngestedOn):
        if debug: print("[listing] ","setLastIngestedOn (unique): ", unique)
        if debug: print("[listing] ","setLastIngestedOn (lastIngestedOn): ", lastIngestedOn)
        values = lastIngestedOn, unique
        cursor.execute("""
        UPDATE rentals SET lastIngestedOn = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","setLastIngesttedOn ","updated successfully. ")

    def setLocZip(self, unique, locZip):
        if debug: print("[listing] ","setLocZip (unique): ", unique)
        if debug: print("[listing] ","setLocZip (arg): ", locZip)
        values = locZip, unique
        cursor.execute("""
        UPDATE rentals SET locZip = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","setLocZip ","updated successfully. ")

    def setLocCity(self, unique, locCity):
        if debug: print("[listing] ","locCity (unique): ", unique)
        if debug: print("[listing] ","locCity (arg): ", locCity)
        values = locCity, unique
        cursor.execute("""
        UPDATE rentals SET locCity = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","locCity ","updated successfully. ")

    def setLocDesc(self, unique, locDesc):
        if debug: print("[listing] ","locDesc (unique): ", unique)
        if debug: print("[listing] ","locDesc (arg): ", locDesc)
        values = locDesc, unique
        cursor.execute("""
        UPDATE rentals SET locDesc = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","locDesc ","updated successfully. ")

    def setPrice(self, unique, price):
        if debug: print("[listing] ","price (unique): ", unique)
        if debug: print("[listing] ","price (arg): ", price)
        values = price, unique
        cursor.execute("""
        UPDATE rentals SET price = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","price ","updated successfully. ")

    def setBedrooms(self, unique, bedrooms):
        if debug: print("[listing] ","bedrooms (unique): ", unique)
        if debug: print("[listing] ","bedrooms (arg): ", bedrooms)
        values = bedrooms, unique
        cursor.execute("""
        UPDATE rentals SET bedrooms = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","bedrooms ","updated successfully. ")

    def setBathrooms(self, unique, bathrooms):
        if debug: print("[listing] ","bathrooms (unique): ", unique)
        if debug: print("[listing] ","bathrooms (arg): ", bathrooms)
        values = bathrooms, unique
        cursor.execute("""
        UPDATE rentals SET bathrooms = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","bathrooms ","updated successfully. ")

    def setDescription(self, unique, description):
        if debug: print("[listing] ","description (unique): ", unique)
        if debug: print("[listing] ","description (arg): ", description)
        values = description, unique
        cursor.execute("""
        UPDATE rentals SET description = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","description ","updated successfully. ")

    def setUrl(self, unique, url):
        if debug: print("[listing] ","url (unique): ", unique)
        if debug: print("[listing] ","url (arg): ", url)
        values = url, unique
        cursor.execute("""
        UPDATE rentals SET url = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","url ","updated successfully. ")

    def setType(self, unique, type):
        if debug: print("[listing] ","type (unique): ", unique)
        if debug: print("[listing] ","type (arg): ", type)
        values = type, unique
        cursor.execute("""
        UPDATE rentals SET type = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","type ","updated successfully. ")

    def setImages(self, unique, images):
        if debug: print("[listing] ","images (unique): ", unique)
        if debug: print("[listing] ","images (arg): ", images)
        values = images, unique
        cursor.execute("""
        UPDATE rentals SET images = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","images ","updated successfully. ")

    def setFeaturedImage(self, unique, featuredImage):
        if debug: print("[listing] ","featuredImage (unique): ", unique)
        if debug: print("[listing] ","featuredImage (arg): ", featuredImage)
        values = featuredImage, unique
        cursor.execute("""
        UPDATE rentals SET featuredImage = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","featuredImage ","updated successfully. ")

    def setPetFriendly(self, unique, petFriendly):
        if debug: print("[listing] ","petFriendly (unique): ", unique)
        if debug: print("[listing] ","petFriendly (arg): ", petFriendly)
        values = petFriendly, unique
        cursor.execute("""
        UPDATE rentals SET petFriendly = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","petFriendly ","updated successfully. ")

    def setFurnished(self, unique, furnished):
        if debug: print("[listing] ","furnished (unique): ", unique)
        if debug: print("[listing] ","furnished (arg): ", furnished)
        values = furnished, unique
        cursor.execute("""
        UPDATE rentals SET furnished = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","furnished ","updated successfully. ")

    def setCurrentlyAvailable(self, unique, currentlyAvailable):
        if debug: print("[listing] ","currentlyAvailable (unique): ", unique)
        if debug: print("[listing] ","currentlyAvailable (arg): ", currentlyAvailable)
        values = currentlyAvailable, unique
        cursor.execute("""
        UPDATE rentals SET currentlyAvailable = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","currentlyAvailable ","updated successfully. ")

    def setVendor(self, unique, vendor):
        if debug: print("[listing] ","vendor (unique): ", unique)
        if debug: print("[listing] ","vendor (arg): ", vendor)
        values = vendor, unique
        cursor.execute("""
        UPDATE rentals SET vendor = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","vendor ","updated successfully. ")

    def setScanner(self, unique, scanner):
        if debug: print("[listing] ","scanner (unique): ", unique)
        if debug: print("[listing] ","scanner (arg): ", scanner)
        values = scanner, unique
        cursor.execute("""
        UPDATE rentals SET scanner = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","scanner ","updated successfully. ")

    def setSquareFeet(self, unique, squareFeet):
        if debug: print("[listing] ","squareFeet (unique): ", unique)
        if debug: print("[listing] ","squareFeet (arg): ", squareFeet)
        values = squareFeet, unique
        cursor.execute("""
        UPDATE rentals SET squareFeet = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","squareFeet ","updated successfully. ")

    def setDeposit(self, unique, deposit):
        if debug: print("[listing] ","deposit (unique): ", unique)
        if debug: print("[listing] ","deposit (arg): ", deposit)
        values = deposit, unique
        cursor.execute("""
        UPDATE rentals SET deposit = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","deposit ","updated successfully. ")

    def setLease(self, unique, lease):
        if debug: print("[listing] ","lease (unique): ", unique)
        if debug: print("[listing] ","lease (arg): ", lease)
        values = lease, unique
        cursor.execute("""
        UPDATE rentals SET lease = ? WHERE id = ?;
        """, values)
        connection.commit()
        if debug: print("[listing] ","lease ","updated successfully. ")

    def new_listing(self, FirstIngestedOn, LastIngestedOn, LocZip, LocCity, LocDesc, price, bedrooms, bathrooms, description, url, type, images, FeaturedImage, PetFriendly, furnished, CurrentlyAvailable, vendor, scanner, SquareFeet, deposit, lease):
        values = FirstIngestedOn, LastIngestedOn, LocZip, LocCity, LocDesc, price, bedrooms, bathrooms, description, url, type, images, FeaturedImage, PetFriendly, furnished, CurrentlyAvailable, vendor, scanner, SquareFeet, deposit, lease
        cursor.execute("""
        INSERT INTO rentals (
            FirstIngestedOn, 
            LastIngestedOn, 
            LocZip, 
            LocCity, 
            LocDesc,    
            price, 
            bedrooms, 
            bathrooms, 
            description, 
            url, 
            type, 
            images, 
            FeaturedImage, 
            PetFriendly, 
            furnished, 
            CurrentlyAvailable, 
            vendor, 
            scanner, 
            SquareFeet, 
            deposit, 
            lease                       
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)
        connection.commit()
        print("[listing] New listing successfully added.")

    def find_listing_by_url(self, url):
        if debug: connection.set_trace_callback(print)
        cursor.execute("""
        SELECT id FROM rentals 
        WHERE url = ? """, (str(url),))
        results = cursor.fetchall()
        if len(results)==0:
            # print("No data returned.")
            self.exists = False
        else:
            self.exists = True
            self.id_number = results[0]

    def find_listing_by_search(self, locDesc, locCity, locZip):
        if debug: connection.set_trace_callback(print)
        if locCity == "Shores, WA":
            locCity == "Ocean Shores, WA"
        search = locDesc, locCity, locZip
        print("[listing] ",search)
        cursor.execute("""
        SELECT id FROM rentals 
        WHERE
            LocDesc = ? AND 
            LocCity = ? AND 
            LocZip = ? """, search)
        results = cursor.fetchall()
        if len(results)==0:
            # print("No data returned.")
            self.exists = False
        else:
            self.exists = True
            self.id_number = results[0]

    def get_listing_price(self, id_number):
        if debug: connection.set_trace_callback(print)
        cursor.execute("""
        SELECT price FROM rentals WHERE id = {}
        """.format(id_number))
        results = cursor.fetchone()
        if len(results)==0:
            self.price = 0
        else:
            self.price = results[0]

    def set_listing_price(self, price):
        values = price, self.id_number
        if debug: connection.set_trace_callback(print)
        cursor.execute("""
        UPDATE rentals SET price = ? WHERE id = ?
        """, values)
        connection.commit()
        print("[listing] Price udpated successfully.")

    def set_square_feet(self, squareFeet):
        values = squareFeet, self.id_number
        if debug: connection.set_trace_callback(print)
        cursor.execute("""
        UPDATE rentals SET SquareFeet = ? WHERE id = ?
        """, values)
        connection.commit()
        print("[listing] Square feet udpated successfully.")

    def set_currently_available(self):
        values = "yes", self.id_number
        cursor.execute("""
        UPDATE rentals SET CurrentlyAvailable = ? WHERE id = ?
        """, values)
        connection.commit()
        print("[listing] Availability status has been updated. ")

    def set_last_ingested(self, lastIngestion):
        if debug: connection.set_trace_callback(print)
        values = lastIngestion, self.id_number
        cursor.execute("""
        UPDATE rentals SET LastIngestedOn = ? WHERE id = ?
        """, values)
        connection.commit()
        print("[listing] LastIngestedIn updated successfully.")

    def find_listing_by_locZip(self, locZip):
        cursor.execute("""
        SELECT id FROM rentals WHERE LocZip = {} 
        """.format(locZip))
        results = cursor.fetchone()
        self.id_number = results[0]

    def mark_missing_unavailable(self, vendor, lastIngestedOn):
        values = vendor, lastIngestedOn
        cursor.execute("""
        UPDATE rentals SET currentlyAvailable = "no" 
        WHERE vendor = ? AND LastIngestedOn < ?;
        """, values)
        connection.commit()
        print("[listing] obsolete records updated.")

    def load_listing(self, id_number):
        try:
            cursor.execute("""
            SELECT id, FirstIngestedOn, LastIngestedOn, LocZip, LocCity, LocDesc, price, bedrooms, bathrooms, description, url, type, images, FeaturedImage, PetFriendly, furnished, CurrentlyAvailable, vendor, scanner, SquareFeet, deposit, lease FROM rentals WHERE id = {}              
            """.format(id_number))
            results = cursor.fetchone()
            if len(results)==0:
                self.exists = False
            else:
                self.id_number = results[0]
                self.firstIngestedOn = results[1]
                self.lastIngestedOn = results[2]
                self.locZip = results[3]
                self.locCity = results[4]
                self.locDesc = results[5]
                self.price = results[6]
                self.bedrooms = results[7]
                self.bathrooms = results[8]
                self.description = results[9]
                self.url = results[10]
                self.type = results[11]
                self.images = results[12]
                self.featuredImage = results[13]
                self.petFriendly = results[14]
                self.furnished = results[15]
                self.currentlyAvailable = results[16]
                self.vendor = results[17]
                self.scanner = results[18]
                self.squareFeet = results[19]
                self.deposit = results[20]
                self.lease = results[21]
                self.exists = True
        except:
            self.exists = False
    
    def find_all_empty_zips(self):
        cursor.execute("""
            SELECT id, LocCity FROM rentals WHERE LocZip = "";
        """)
        results = cursor.fetchall()
        self.results = results
    
    def update_zip(self, id_number, zip):
        values = int(zip), id_number
        print("[listing] ",values)
        cursor.execute("""
            UPDATE rentals SET LocZip = ? WHERE id = ?;
        """, values)
        connection.commit()
        print("[listing] Zip code updated successfully.")

    def update_available(self):
        cursor.execute("""
        UPDATE rentals
        SET CurrentlyAvailable = 'no'
        WHERE
        date(LastIngestedOn) > date(FirstIngestedOn)
        AND date(LastIngestedOn) < date('now', '-3 days');       
        """)
        connection.commit()
        print("[listing] Availability updated, marking units that haven't been seen in a few days.")
    
    def update_days_on_market(self):
        cursor.execute("""
        UPDATE rentals
        SET DaysOnMarket = julianday(LastIngestedOn) - julianday(FirstIngestedOn);
        """)
        connection.commit()
        print("[listing] Updated daysOnMarket.")