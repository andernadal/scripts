#!/usr/bin/env python3

import MySQLdb
import sys
import time
import datetime

print("Starting...")
print(datetime.datetime.now())

try:
    gerencia = MySQLdb.connect("host","user","password","database")
    esp = MySQLdb.connect("host","user","password","database")
    net = MySQLdb.connect("host","user","password","database")

    cursor_gerencia = gerencia.cursor()
    cursor_esp = esp.cursor()
    cursor_net = net.cursor()
except:
    print("Failed connecting to MySQL Database!")
    sys.exit(1)

#Change export do D, "DOING", freezing the record to manipulate
sql_marca_esp = "UPDATE radius.radacct set export='D'  where export='N' and vrf='CGNAT_ESP' and acctstoptime is not NULL"
sql_marca_net = "UPDATE radius.radacct set export='D'  where export='N' and vrf='CGNAT_NET' and acctstoptime is not NULL"

try:
	print("Changing the record...")
	cursor_gerencia.execute(sql_marca_esp)
	cursor_gerencia.execute(sql_marca_net)
#	gerencia.commit()
except: 
	print("Failed changing the record to manipulate!")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	net.close()
	sys.exit(1)


sql_select_esp = "SELECT acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf from radius.radacct where export='D' and vrf='CGNAT_ESP'"

try:
	print("Selecting records - ESP...")
	cursor_gerencia.execute(sql_select_esp)
	count_esp = cursor_gerencia.rowcount
	result_esp = cursor_gerencia.fetchall()
	print(count_esp)
except:
	print("Failed selecting records - ESP!")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	net.close()
	sys.exit(1)
	

sql_select_net = "SELECT acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf from radius.radacct where export='D' and vrf='CGNAT_NET'"

try:
	print("Selecting records - NET...")
	cursor_gerencia.execute(sql_select_net)
	count_net = cursor_gerencia.rowcount
	result_net = cursor_gerencia.fetchall()
	print(count_net)
except:
	print("Failed selecting records - NET!")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	net.close()
	sys.exit(1)
	

#Insert na base ESP e net
sql_insert_esp = "INSERT into esp.radacct (acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
controle_esp=2
if count_esp >= 1 :
	try: 
		print("Migrating records - ESP...")
		cursor_esp.executemany(sql_insert_esp,result_esp)
		print(cursor_esp.rowcount)
		controle_esp=0
	except:
		print("Failed migrating records - ESP!")
		controle_esp=1
else :
	print("No record to work!")


sql_insert_net = "INSERT into net.radacct (acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

controle_net=2

if count_net >= 1 :
	try: 
		print("Migrating records - NET...")
		cursor_net.executemany(sql_insert_net,result_net)
		print(cursor_net.rowcount)
		controle_net=0
	except: 
		print("Failed migrating records - NET!")
		controle_net=1
else :
	print("No record to work!")


#Validando 
if (controle_esp == 0 and count_esp >= 1) :
	sql_update_esp = "UPDATE radius.radacct set export='Y' where export='D' and vrf='CGNAT_ESP'"
	try:
		print("Updating records - ESP...")
		cursor_gerencia.execute(sql_update_esp)
		gerencia.commit()
		esp.commit()
	except:
		print("Failed updating record - database gerencia!")
		gerencia.rollback()
		esp.rollback()

if (controle_net == 0 and count_net >= 1) :
	sql_update_net = "UPDATE radius.radacct set export='Y' where export='D' and vrf='CGNAT_NET'"
	try:
		print("Updating records - NET...")
		cursor_gerencia.execute(sql_update_net)
		gerencia.commit()
		net.commit()
	except:
		print("Failed updating record - database gerencia!")
		gerencia.rollback()
		net.rollback()

print("Closing connections...")
gerencia.close()
esp.close()
net.close()
print(datetime.datetime.now())
print("Done!")
