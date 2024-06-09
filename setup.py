# setup.py

# check for database
import os
import sqlite3
from sqlite3 import Error
import sys
import os
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, libdir)
from class_listing import Listing

print("Welcome to chickadee! This collection of python files indexes rental listings on websites in Grays Harbor County, WA.")
print("-------------------------")
print("Let's see if we can set this up for you.")
print("Checking database file ....")
db = "db/db.sqlite3"
if os.path.exists(db):
    print("Looks like the database already exists. That's great! Moving on ...")
else:
    # create database
    print("I don't see a database file, so I'll create an empty one now:")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    if os.path.exists("db/newdb.sql"):
        with open("db/newdb.sql", "r") as sql_file:
            sql = sql_file.read()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        print("OK, a new empty database is set up and ready to rock.")
    else:
        print("SQL script to initiate the database not found. Are you sure you cloned the git repo?")
        exit()

print("Last step - you'll have to manually run the requirements.text file.")
print("If you have multiple versions of python, run:")
print("python3 -m pip install -r requirements.txt")
print("Otherwise, run:")
print("python -m pip install -r requirements.txt")
print("When done, run main.py to get started.")
print("That's it! Setup is complete. ")

# index scanners
# scanners = os.listdir("scanners/")
# for scanner in scanners:
    # get list of scanner files
    # get list of scanners in db