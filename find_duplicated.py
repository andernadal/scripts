#!/usr/bin/env python3.5

import sys
import logging
from netmiko import Netmiko
from getpass import getpass

def duplicated(x):
    _size = len(x)
    repetidos = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repetidos:
                repetidos.append(x[i])
    for j in range(len(repetidos)):
        print(repetidos[j])

    return 0


CONNECTED = []
AUX = []
HOST = "asr9k"
COMMAND = "show subscriber session all username  | inc pppoe | util cut field 1 delimiter PE"

USER = input("Enter username: ")
PASSWORD = getpass("Enter password: ")

my_device = {
    'host': HOST,
    'username': USER,
    'password': PASSWORD,
    'secret': PASSWORD,
    'device_type': 'cisco_xr',
}

try:
    print("Connecting...  "+ HOST +"\n")
    net_connect = Netmiko(**my_device)
    net_connect.enable()
    output = net_connect.send_command(COMMAND)
    print("Working...\n")
    subscribers = list(output.split(" "))
    subscribers.sort()
except:
     print("Failed connecting!")
     sys.exit(1)


print("Finding duplicated subscribers...\n")
for i in range(len(subscribers)):
    if subscribers[i] == '':
     AUX=subscribers[i]
    else:
     CONNECTED.append(subscribers[i])

duplicated(CONNECTED)

print("Closing connections...")
net_connect.disconnect()
print("Done!")

