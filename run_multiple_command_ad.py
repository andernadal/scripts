import sys
import logging
import getpass
import time
from colorama import Fore, Back, Style
from netmiko import Netmiko
from getpass import getpass
import ip_functions

LOG = 0
APP = ""

#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

if (len(sys.argv) >= 2) and (sys.argv[1] == "log"):
    LOG = 1
    if (len(sys.argv) >= 3) and  (sys.argv[2] == "before"):
        APP = ".before"
    if (len(sys.argv) >= 3) and  (sys.argv[2] == "after"):
        APP = ".after"
else:
    LOG = 0


try:
    fd= open("devices.txt","r")
except:
    print(Fore.RED + "File devices.txt not found!")
    print(Style.RESET_ALL)
    sys.exit(1)

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")

for HOST in fd:
    HOST=HOST.strip()
    if(ip_functions.lookup(HOST) != 0 or ip_functions.ping(HOST) != 0):
        print(Fore.RED + HOST,"not found or not reachable via ICMP!")
        print(Style.RESET_ALL)
    else:

        if (LOG == 1):
            try:
                log_file = open(HOST + ".log" + APP, "w")
            except:
                print(Fore.RED + "Failed creating log file!")
                print(Style.RESET_ALL)
                sys.exit(1)

        try:
            fc = open("comandos.txt", "r")
        except:
            print(Fore.RED + "File comandos.txt not found!")
            print(Style.RESET_ALL)
            sys.exit(1)

        print(Fore.CYAN + "Connecting...  "+ HOST +"\n")
        print(Style.RESET_ALL)

        my_device = {
            'ip': HOST,
            'username': USER,
            'password': PASSWORD,
            'secret': PASSWORD,
           #'device_type': 'cisco_xe',
            'device_type': 'juniper_junos',
            'global_delay_factor': 3,
            }

        try:
            net_connect = Netmiko(**my_device)
            net_connect.enable()
            try:
                for COMANDO in fc:
                    output = net_connect.send_command(COMANDO)
                    if (LOG == 1) :
                        log_file.write(COMANDO)
                        log_file.write(output)
                    else :
                        print(COMANDO,"\n")
                        print(output)

                if (LOG == 1):
                    log_file.close()

                net_connect.disconnect()
            except:
                print(Fore.RED + "Failed sending commands!")
                print(Style.RESET_ALL)
                net_connect.disconnect()
        except:
            print(Fore.RED + "Failed connecting!")
            print(Style.RESET_ALL)


print("Closing connections...")
fd.close()
fc.close()
print("Done!")

