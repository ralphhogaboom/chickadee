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

db = "db/db.sqlite3"
if os.path.exists(db):
    print("Database already exists, moving on ...")
else:
    # create database
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
    else:
        print("SQL script to initiate the database not found. Are you sure you cloned the git repo?")
        exit()

# index scanners
# scanners = os.listdir("scanners/")
# for scanner in scanners:
    # get list of scanner files
    # get list of scanners in db