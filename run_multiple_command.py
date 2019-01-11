import sys
import logging
import getpass
import time
from netmiko import Netmiko
from getpass import getpass

LOG = 0

#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

if (len(sys.argv) >= 2) and (sys.argv[1] == "log"):
    LOG = 1
else:
    LOG = 0


try:
    fd= open("devices.txt","r")
except:
    print("File devices.txt not found!")
    sys.exit(1)

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")

for HOST in fd:

    HOST=HOST.strip()

    if (LOG == 1):
        try:
            log_file = open(HOST + ".log", "w")
        except:
            print("Failed creating log file!")
            sys.exit(1)

    try:
        fc = open("comandos.txt", "r")
    except:
        print("File comandos.txt not found!")
        sys.exit(1)

    print("Connecting...  "+ HOST +"\n")

    my_device = {
        'ip': HOST,
        'username': USER,
        'password': PASSWORD,
        'secret': PASSWORD,
        'device_type': 'cisco_ios',
                }

#'global_delay_factor': 2,

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
            print("Failed sending commands!")
            net_connect.disconnect()
            sys.exit(1)
    except:
        print("Failed connecting!")
        sys.exit(1)


print("Closing connections...")
fd.close()
fc.close()
print("Done!")

