import sqlite3
from sqlite3 import Error

debug = False

global db
db = "C:/Users/ralph/Documents/Antsy Chickadee/antsy chickadee 2405.sqlite3"
connection = sqlite3.connect(db)
cursor = connection.cursor()

class Listing:
    def __init__(self, id_number=-1):
        self.id_number = id
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
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
        print("New listing successfully added.")

    def find_listing_by_search(self, locDesc, locCity, locZip):
        if debug: connection.set_trace_callback(print)
        search = locDesc, locCity, locZip
        print(search)
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
        print("Price udpated successfully.")

    def set_square_feet(self, squareFeet):
        values = squareFeet, self.id_number
        if debug: connection.set_trace_callback(print)
        cursor.execute("""
        UPDATE rentals SET SquareFeet = ? WHERE id = ?
        """, values)
        connection.commit()
        print("Square feet udpated successfully.")

    def set_currently_available(self):
        values = "yes", self.id_number
        cursor.execute("""
        UPDATE rentals SET CurrentlyAvailable = ? WHERE id = ?
        """, values)
        connection.commit()
        print("Availability status has been updated. ")

    def set_last_ingested(self, lastIngestion):
        if debug: connection.set_trace_callback(print)
        values = lastIngestion, self.id_number
        cursor.execute("""
        UPDATE rentals SET LastIngestedOn = ? WHERE id = ?
        """, values)
        connection.commit()
        print("LastIngestedIn updated successfully.")

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
        print("obsolete records updated.")

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