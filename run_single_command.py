import sys
import logging
from netmiko import Netmiko
from getpass import getpass
import ip_functions 


#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

if len(sys.argv) == 1 :
    HOST = input("Enter hostname: ")
elif len(sys.argv) == 2 :
    HOST = sys.argv[1]

if(ip_functions.lookup(HOST) != 0):
    print("Host not found!")
    sys.exit(1)

if(ip_functions.ping(HOST) != 0):
    print("Host not reachable via ICMP!")
    sys.exit(1)

try:
    fc= open("comandos.txt","r")
except:
    print("File comandos.txt not found!")
    sys.exit(1)

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")

my_device = {
    'host': HOST,
    'username': USER,
    'password': PASSWORD,
    'secret': PASSWORD,
#    'device_type': 'cisco_xr',
    'device_type': 'juniper_junos',
}

try:
    net_connect = Netmiko(**my_device)
    net_connect.enable()
    print("Connecting...  "+ HOST +"\n")
    try:
         for COMANDO in fc:
            output = net_connect.send_command(COMANDO)
            print(COMANDO)
            print(output)
         fc.close()
    except:
     print("File comandos.txt not found!") 
except:
     print("Failed connecting!") 
     sys.exit(1)

print("Closing connections...")
net_connect.disconnect()
print("Done!")

