
import csv
import MySQLdb
import sys
import logging
import getpass
import time
import datetime

print("Starting...")
print(datetime.datetime.now())

try:
    fd= open("result.csv","r")
except:
    print("File result.csv not found!")
    sys.exit(1)
fd.close()

try:
    mysql = MySQLdb.connect("host","user","password","database" )
    cursor = mysql.cursor()
except:
    print("MySQL connection failed!")
    mysql.close()
    sys.exit(1)


sql_insert = "INSERT into inventario.inventario (host, v1, v2, v3, v4) values (%s,%s,%s,%s,%s)"
try:
    with open('result.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        print("Inserting record...")
        for row in readCSV:
            cursor.execute(sql_insert,row)
except:
    print("Failed reading result.csv!")

print("Closing...")
mysql.commit()
mysql.close()
print(datetime.datetime.now())
print ("Done!")
