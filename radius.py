#!/usr/bin/env python3

import MySQLdb
import sys
import time
import datetime

print("Iniciando:")
print(datetime.datetime.now())

gerencia = MySQLdb.connect("localhost","radius","radiator","radius" )
esp = MySQLdb.connect("localhost","esp","radiator","esp" )
novanet = MySQLdb.connect("localhost","novanet","radiator","novanet" )

cursor_gerencia = gerencia.cursor()
cursor_esp = esp.cursor()
cursor_novanet = novanet.cursor()

#Altera export para D, "Doing" e com isso impede que novos registros sejam manipulados
sql_marca_esp = "UPDATE radius.radacct set export='D'  where export='N' and vrf='CGNAT_ESP' and acctstoptime is not NULL"
sql_marca_novanet = "UPDATE radius.radacct set export='D'  where export='N' and vrf='CGNAT_NOVANET' and acctstoptime is not NULL"

try:
	print("Marcando registros")
	cursor_gerencia.execute(sql_marca_esp)
	cursor_gerencia.execute(sql_marca_novanet)
#	gerencia.commit()
except: 
	print("Falha na marcacao dos registros a serem manipulados")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	novanet.close()
	sys.exit(1)


sql_select_esp = "SELECT acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf from radius.radacct where export='D' and vrf='CGNAT_ESP'"

try:
	print("Selecionando registros ESP:")
	cursor_gerencia.execute(sql_select_esp)
	count_esp = cursor_gerencia.rowcount
	result_esp = cursor_gerencia.fetchall()
	print(count_esp)
except:
	print("Falha na selecao dos registros a serem manipulados ESP")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	novanet.close()
	sys.exit(1)
	

sql_select_novanet = "SELECT acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf from radius.radacct where export='D' and vrf='CGNAT_NOVANET'"

try:
	print("Selecionando registros Novanet:")
	cursor_gerencia.execute(sql_select_novanet)
	count_novanet = cursor_gerencia.rowcount
	result_novanet = cursor_gerencia.fetchall()
	print(count_novanet)
except:
	print("Falha na selecao dos registros a serem manipulados Novanet")
	gerencia.rollback()
	gerencia.close()
	esp.close()
	novanet.close()
	sys.exit(1)
	

#Insert na base ESP e Novanet
sql_insert_esp = "INSERT into esp.radacct (acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
controle_esp=2
if count_esp >= 1 :
	try: 
		print("Migrando registros ESP:")
		cursor_esp.executemany(sql_insert_esp,result_esp)
		print(cursor_esp.rowcount)
		controle_esp=0
	except: 
		print("Erro na atualizacao da base ESP")
		controle_esp=1
else :
	print("Sem registros para migrar na ESP")


sql_insert_novanet = "INSERT into novanet.radacct (acctsessionid, acctuniqueid, username, groupname, realm, nasipaddress, nasportid, nasporttype, acctstarttime, acctstoptime, acctsessiontime, acctauthentic, connectinfo_start, connectinfo_stop, acctinputoctets, acctoutputoctets, calledstationid, callingstationid, acctterminatecause, servicetype, framedprotocol, framedipaddress, acctstartdelay, acctstopdelay, xascendsessionsvrkey, framedip6address, framedinterfaceid, delegatedipv6prefix, framedip6addresscisco, vrf) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

controle_novanet=2

if count_novanet >= 1 :
	try: 
		print("Migrando registros Novanet:")
		cursor_novanet.executemany(sql_insert_novanet,result_novanet)
		print(cursor_novanet.rowcount)
		controle_novanet=0
	except: 
		print("Erro na atualizacao da base ESP")
		controle_novanet=1
else :
	print("Sem registros para migrar na Novanet")


#Validando 
if (controle_esp == 0 and count_esp >= 1) :
	sql_update_esp = "UPDATE radius.radacct set export='Y' where export='D' and vrf='CGNAT_ESP'"
	try:
		print("Atualizando registros ESP")
		cursor_gerencia.execute(sql_update_esp)
		gerencia.commit()
		esp.commit()
	except:
		print("Erro na atualizacao dos valores da base gerencia")
		gerencia.rollback()
		esp.rollback()

if (controle_novanet == 0 and count_novanet >= 1) :
	sql_update_novanet = "UPDATE radius.radacct set export='Y' where export='D' and vrf='CGNAT_NOVANET'"
	try:
		print("Atualizando registros Novanet")
		cursor_gerencia.execute(sql_update_novanet)
		gerencia.commit()
		novanet.commit()
	except:
		gerencia.rollback()
		novanet.rollback()

#Fechando tudo
gerencia.close()
esp.close()
novanet.close()

print("Finalizando:")
print(datetime.datetime.now())
