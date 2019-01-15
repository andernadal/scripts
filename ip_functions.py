import socket
from scapy.all import *


def ping(HOST):
    TIMEOUT = 2
    conf.verb = 0
    packet = IP(dst=HOST, ttl=20)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if not (reply is None):
        return 0
    else:
        return 1

def lookup(HOST):

    try:
        HOST_IP = socket.gethostbyname(HOST)
        return 0
    except socket.gaierror:
        return 1
