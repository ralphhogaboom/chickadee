# setup.py

# check for database
import os
import sqlite3
from sqlite3 import Error

db = "db/db.sqlite3"
if os.path.exists(db):
    print("Database already exists, moving on ...")
else:
    # create database
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    if os.path.exists("db/create.sql"):
        with open("db/create.sql", "r") as sql_file:
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
