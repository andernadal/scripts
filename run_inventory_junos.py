import sys
import logging
import getpass
import time
from colorama import Fore, Back, Style
from getpass import getpass
import ip_functions
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml
import sys


if (len(sys.argv) >= 2):
    HOST = sys.argv[1]
else:
    print(Fore.RED + "No Hostname, please give the hostname to connect!")
    print(Style.RESET_ALL)
    sys.exit(1)

try:
    with open("table_views.yml", 'r') as tvs:
        globals().update(FactoryLoader().load(yaml.load(tvs)))

except:
    print(Fore.RED + "File table_views.yml not found!")
    print(Style.RESET_ALL)
    sys.exit(1)

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")
orig_stdout = sys.stdout

HOST=HOST.strip()
FILE_INVENTORY = "inventory-" + HOST + ".csv"

if(ip_functions.lookup(HOST) != 0 or ip_functions.ping(HOST) != 0):
    print(Fore.RED + HOST,"not found or not reachable via ICMP!")
    print(Style.RESET_ALL)
else:

        try:
            sys.stdout = orig_stdout
            f = open(FILE_INVENTORY, 'w')
            print(Fore.CYAN + "Connecting...  " + HOST + "\n")
            print(Style.RESET_ALL)

            with Device(host=HOST, user=USER, password=PASSWORD, gather_facts=False) as dev:

                 inv = ChassisInventoryTable(dev)
                 inv.get()
                #sys.stdout = f

                 for item in inv:
                    print("Router Name",",","Item Name",",","Description",",","Serial Number",",","Part Number",",","Version",",","Model Number")
                    print(HOST,",",item.name,",",item.desc,",",item.sn)

                    for i in [item.MDP, item.FPM, item.FDM, item.PEM, item.RE, item.CB]:
                        for j in i:
                            print(HOST,",",j.name,",",j.desc,",",j.sn,",",j.pn,",",j.ver,",",j.model)
                    for k in item.FPC:
                        print(HOST,",",k.name,",",k.desc,",",k.sn,",",k.pn,",",k.ver,",",j.model)
                        #colocar um if para ver se tem MIC ou PIC e seguir em frente
                        if not k.MIC:
                            for m in k.PIC:
                                print(HOST,",",m.name,",",m.desc,",",m.sn,",",m.pn)
                                for n in m.PORT:
                                    print(HOST,",",n.name,",",n.desc,",",n.sn,",",n.pn,",",n.ver)
                        else:
                         for l in k.MIC:
                            print(HOST,",",l.name,",",l.desc,",",l.sn,",",l.pn,",",l.ver,",",j.model)
                            for m in l.PIC:
                                print(HOST,",",m.name,",",m.desc,",",m.sn,",",m.pn)
                                for n in m.PORT:
                                    print(HOST,",",n.name,",",n.desc,",",n.sn,",",n.pn,",",n.ver)

                 f.close()

        except:
                sys.stdout = orig_stdout
                print(Fore.RED + "Connection Fail !")
                print(Style.RESET_ALL)

sys.stdout = orig_stdout
print(Fore.LIGHTBLUE_EX + "Closing connections...\n")
print(Fore.LIGHTBLUE_EX + "Done. Check inventory.csv !\n")
print(Style.RESET_ALL)