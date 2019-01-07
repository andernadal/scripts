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
    net_connect = Netmiko(**my_device)
    try:
         net_connect.enable()
         output = net_connect.send_config_from_file("config_file.txt")
         print(output)
    except:
     print("Falha na configuracao") 
except:
     print("Erro na conexao") 
     sys.exit(1)

net_connect.disconnect()

