
import csv
import MySQLdb
import sys
import logging
import getpass
import time
import datetime

print("Iniciando:")
print(datetime.datetime.now())

try:
    fd= open("result.csv","r")
except:
    print("Arquivo de resultados nao existe")
    sys.exit(1)
fd.close()

try:
    mysql = MySQLdb.connect("host","user","password","database" )
    cursor = mysql.cursor()
except:
    print("Falha na conexao com o MySQL")
    mysql.close()
    sys.exit(1)


sql_insert = "INSERT into inventario.inventario (host, v1, v2, v3, v4) values (%s,%s,%s,%s,%s)"
try:
    with open('result.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        print("Inserindo registros:")
        for row in readCSV:
            cursor.execute(sql_insert,row)
except:
    print("Falha na leitura do arquivo")

mysql.commit()
mysql.close()

print("Finalizando:")
print(datetime.datetime.now())
print ("Done")
