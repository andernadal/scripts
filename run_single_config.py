import sys
from netmiko import Netmiko
from getpass import getpass

HOST = input("Enter hostname: ")
USER = input("Enter username: ")

my_device = {
    'host': HOST,
    'username': USER,
    'password': getpass(),
    'device_type': 'cisco_nxos',
    # Increase (essentially) all sleeps by a factor of 2
    #'global_delay_factor': 2,
}
try:
    fc= open("config_file.txt","r")
except:
    print("File config_file.txt not found!")
    sys.exit(1)


try:
    net_connect = Netmiko(**my_device)
    print("Connecting...  "+ HOST +"\n")
    try:
         net_connect.enable()
         output = net_connect.send_config_from_file("config_file.txt")
         print(output)
    except:
     print("Failed configuring!") 
except:
     print("Failed connecting!") 
     sys.exit(1)

print("Closing connections...")
net_connect.disconnect()
print("Done!")

