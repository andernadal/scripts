import sys
import logging

from netmiko import Netmiko
from getpass import getpass

#logging.basicConfig(filename='test.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")
if len(sys.argv) == 1 :
    HOST = input("Enter hostname: ")
elif len(sys.argv) == 2 :
    HOST = sys.argv[1]

try:
    fc= open("comandos.txt","r")
except:
    print("Arquivo de comandos nao existe")
    sys.exit(1)

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")

my_device = {
    'host': HOST,
    'username': USER,
    'password': PASSWORD,
    'secret': PASSWORD,
#    'device_type': 'cisco_xr',
    'device_type': 'extreme',
}

try:
    net_connect = Netmiko(**my_device)
    net_connect.enable()
    try:
         for COMANDO in fc:
            output = net_connect.send_command(COMANDO)
            print(COMANDO)
            print(output)
         fc.close()
    except:
     print("Arquivo de comandos nao existe") 
except:
     print("Erro na conexao") 
     sys.exit(1)

net_connect.disconnect()

