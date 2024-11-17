import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
import sys
import os
import pathlib
from datetime import datetime
from dotenv import load_dotenv

debug = True
load_dotenv()

env_ssh_host=str(os.getenv("ssh_host"))
env_ssh_port=int(os.getenv("ssh_port"))
env_ssh_username=str(os.getenv("ssh_username"))
env_ssh_password=str(os.getenv("ssh_password"))
env_remote_bind_address=os.getenv("db_remote_bind_address")
env_db_host=str(os.getenv("db_host"))
env_db_username=str(os.getenv("db_username"))
env_db_password=str(os.getenv("db_password"))
env_db_port=int(os.getenv("db_port"))
env_db_name=str(os.getenv("db_name"))

class DatabaseManager:
    def __init__(self):
        self.ssh_host = env_ssh_host
        self.ssh_port = env_ssh_port
        self.ssh_username = env_ssh_username
        self.ssh_password = env_ssh_password
        self.db_host = env_db_host
        self.db_port = env_db_port
        self.db_username = env_db_username
        self.db_password = env_db_password
        self.db_name = env_db_name
        self.tunnel = None
        self.connection = None
        self.results = None

    def connect(self):
        if not self.connection:
            self.tunnel = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_username,
                ssh_password=self.ssh_password,
                remote_bind_address=(self.db_host, self.db_port),
            )
            self.tunnel.start()
            self.connection = pymysql.connect(
                host='127.0.0.1',
                port=self.tunnel.local_bind_port,
                user=self.db_username,
                password=self.db_password,
                database=self.db_name,
            )
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        if self.tunnel:
            self.tunnel.stop()
            self.tunnel = None

    def execute_query(self, sql, values=None):
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.fetchall()

class Listing:
    def __init__(self, id_number=-1):
        if debug: print("[listing] ", "Starting log ...")
        self.id_number = id
        self.database = DatabaseManager()

    def createNew(self, unique):
        unique = unique.strip()
        strNow = datetime.today().strftime('%Y-%m-%d')
        values = unique, strNow, strNow
        sql = "INSERT INTO rentals (uniqueValue, firstIngestedOn, lastIngestedOn) VALUES (%s, %s, %s);"
        self.database.execute_query(sql, values)
        if debug: print("[listing] ", "New listing successfully added.")

    def searchUnique(self, unique):
        unique = unique.strip()
        if debug: print("[listing] ","findByUnique (type): ", type(unique))
        if debug: print("[listing] ","findByUnique (value): ", unique)
        values = (unique,)
        sql = "SELECT id FROM rentals WHERE uniqueValue = %s;"
        results = self.database.execute_query(sql, values)
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
        unique = unique[0]
        if debug: print("[listing] ","setLastIngestedOn (unique): ", unique)
        if debug: print("[listing] ","setLastIngestedOn (lastIngestedOn): ", lastIngestedOn)
        values = lastIngestedOn, unique
        sql = ("""
        UPDATE rentals SET lastIngestedOn = %s WHERE id = %s;
        """)
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","setLastIngesttedOn ","updated successfully. ")

    def setLocZip(self, unique, locZip):
        unique = int(unique[0])
        locZip = locZip.strip()
        locZip = int(locZip)
        if debug: print("[listing] POST-SANITIZE ","setLocZip (unique): ", unique)
        if debug: print("[listing] POST-SANITIZE ","setLocZip (arg): ", locZip)
        values = locZip, unique
        sql = """
        UPDATE rentals SET locZip = %s WHERE id = %s and LocZip = 0;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","setLocZip ","updated successfully. ")

    def setLocCity(self, unique, locCity):
        unique = unique[0]
        locCity = locCity.strip()
        locCity = locCity.replace(", WA","")
        locCity = locCity.replace(",  WA","")
        locCity = locCity.replace(", Wa","")
        locCity = locCity.replace(",  Wa","")
        locCity = locCity.replace(", wa","")
        locCity = locCity.replace(",  wa","")
        if debug: print("[listing] ","locCity (unique): ", unique)
        if debug: print("[listing] ","locCity (arg): ", locCity)
        values = locCity, unique
        sql = """
        UPDATE rentals SET locCity = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","locCity ","updated successfully. ")

    def setLocDesc(self, unique, locDesc):
        unique = unique[0]
        locDesc = locDesc.strip()
        if debug: print("[listing] ","locDesc (unique): ", unique)
        if debug: print("[listing] ","locDesc (arg): ", locDesc)
        values = locDesc, unique
        sql = """
        UPDATE rentals SET locDesc = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","locDesc ","updated successfully. ")

    def setPrice(self, unique, price):
        unique = unique[0]
        price = price.strip()
        try:
            price = int(price)
        except:
            price = 0
        if debug: print("[listing] ","price (unique): ", unique)
        if debug: print("[listing] ","price (arg): ", price)
        values = price, unique
        sql = """
        UPDATE rentals SET price = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","price ","updated successfully. ")

    def setBedrooms(self, unique, bedrooms):
        unique = unique[0]
        try:
            bedrooms = int(bedrooms)
            print("Bedrooms is already a number.")
        except:
            bedrooms = bedrooms.strip().lower()
            if "studio" in bedrooms:
                bedrooms = 0
            bedrooms = int(bedrooms)
        if debug: print("[listing] ","bedrooms (unique): ", unique)
        if debug: print("[listing] ","bedrooms (arg): ", bedrooms)
        values = bedrooms, unique
        sql = """
        UPDATE rentals SET bedrooms = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","bedrooms ","updated successfully. ")

    def setBathrooms(self, unique, bathrooms):
        unique = unique[0]
        if type(bathrooms) == str:
            print("Bathrooms is a string.")
            bathrooms = bathrooms.strip()
        bathrooms = float(bathrooms)
        if debug: print("[listing] ","bathrooms (unique): ", unique)
        if debug: print("[listing] ","bathrooms (arg): ", bathrooms)
        values = bathrooms, unique
        sql = """
        UPDATE rentals SET bathrooms = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","bathrooms ","updated successfully. ")

    def setDescription(self, unique, description):
        unique = unique[0]
        description = description.strip()
        if debug: print("[listing] ","description (unique): ", unique)
        if debug: print("[listing] ","description (arg): ", description)
        values = description, unique
        sql = """
        UPDATE rentals SET description = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","description ","updated successfully. ")

    def setUrl(self, unique, url):
        unique = unique[0]
        url = url.strip()
        if debug: print("[listing] ","url (unique): ", unique)
        if debug: print("[listing] ","url (arg): ", url)
        values = url, unique
        sql = """
        UPDATE rentals SET url = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","url ","updated successfully. ")

    def setType(self, unique, type):
        unique = unique[0]
        type = str(type).strip()
        if debug: print("[listing] ","type (unique): ", unique)
        if debug: print("[listing] ","type (arg): ", type)
        values = type, unique
        sql = """
        UPDATE rentals SET type = %s WHERE id = %s AND type <> 'bad_data';
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","type ","updated successfully. ")

    def setImages(self, unique, images):
        unique = unique[0]
        if debug: print("[listing] ","images (unique): ", unique)
        if debug: print("[listing] ","images (arg): ", images)
        values = images, unique
        sql = """
        UPDATE rentals SET images = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","images ","updated successfully. ")

    def setFeaturedImage(self, unique, featuredImage):
        unique = unique[0]
        featuredImage = featuredImage.strip()
        if debug: print("[listing] ","featuredImage (unique): ", unique)
        if debug: print("[listing] ","featuredImage (arg): ", featuredImage)
        values = featuredImage, unique
        sql = """
        UPDATE rentals SET featuredImage = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","featuredImage ","updated successfully. ")

    def setPetFriendly(self, unique, petFriendly):
        unique = unique[0]
        petFriendly = petFriendly.strip()
        if debug: print("[listing] ","petFriendly (unique): ", unique)
        if debug: print("[listing] ","petFriendly (arg): ", petFriendly)
        values = petFriendly, unique
        sql = """
        UPDATE rentals SET petFriendly = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","petFriendly ","updated successfully. ")

    def setFurnished(self, unique, furnished):
        unique = unique[0]
        furnished = furnished.strip()
        if debug: print("[listing] ","furnished (unique): ", unique)
        if debug: print("[listing] ","furnished (arg): ", furnished)
        values = furnished, unique
        sql = """
        UPDATE rentals SET furnished = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","furnished ","updated successfully. ")

    def setCurrentlyAvailable(self, unique, currentlyAvailable):
        unique = unique[0]
        currentlyAvailable = currentlyAvailable.strip()
        if debug: print("[listing] ","currentlyAvailable (unique): ", unique)
        if debug: print("[listing] ","currentlyAvailable (arg): ", currentlyAvailable)
        values = currentlyAvailable, unique
        sql = """
        UPDATE rentals SET currentlyAvailable = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","currentlyAvailable ","updated successfully. ")

    def setVendor(self, unique, vendor):
        unique = unique[0]
        vendor = vendor.strip()
        if debug: print("[listing] ","vendor (unique): ", unique)
        if debug: print("[listing] ","vendor (arg): ", vendor)
        values = vendor, unique
        sql = """
        UPDATE rentals SET vendor = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","vendor ","updated successfully. ")

    def setScanner(self, unique, scanner):
        unique = unique[0]
        scanner = scanner.strip()
        if debug: print("[listing] ","scanner (unique): ", unique)
        if debug: print("[listing] ","scanner (arg): ", scanner)
        values = scanner, unique
        sql = """
        UPDATE rentals SET scanner = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","scanner ","updated successfully. ")

    def setSquareFeet(self, unique, squareFeet):
        unique = unique[0]
        squareFeet = squareFeet.strip()
        if debug: print("[listing] ","squareFeet (unique): ", unique)
        if debug: print("[listing] ","squareFeet (arg): ", squareFeet)
        values = squareFeet, unique
        sql = """
        UPDATE rentals SET squareFeet = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","squareFeet ","updated successfully. ")

    def setDeposit(self, unique, deposit):
        unique = unique[0]
        deposit = deposit.strip()
        if debug: print("[listing] ","deposit (unique): ", unique)
        if debug: print("[listing] ","deposit (arg): ", deposit)
        values = deposit, unique
        sql = """
        UPDATE rentals SET deposit = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)
        if debug: print("[listing] ","deposit ","updated successfully. ")

    def setLease(self, unique, lease):
        unique = unique[0]
        lease = lease.strip()
        if debug: print("[listing] ","lease (unique): ", unique)
        if debug: print("[listing] ","lease (arg): ", lease)
        values = lease, unique
        sql = """
        UPDATE rentals SET lease = %s WHERE id = %s;
        """
        results = self.database.execute_query(sql, values)    
        if debug: print("[listing] ","lease ","updated successfully. ")