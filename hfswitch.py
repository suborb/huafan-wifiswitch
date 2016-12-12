
import socket
from Crypto.Cipher import AES
import base64
import sys


def encrypt(message, passphrase):
    IV = "4528453102574529"
    length = 16 - (len(message) % 16)
    message += chr(length)*length
    aes = AES.new(passphrase, AES.MODE_CBC, IV)
    return base64.b64encode(aes.encrypt(message))

def decrypt(encrypted, passphrase):
    IV = "4528453102574529"
    aes = AES.new(passphrase, AES.MODE_CBC, IV)
    return aes.decrypt(base64.b64decode(encrypted))

def turnOn(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 AT+SOPEN=1\r\n"
    tosend=encrypt(msg,"9521314528002574")
    sock.sendall(tosend)

def turnOff(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 AT+SCLOSE=1\r\n"
    tosend=encrypt(msg,"9521314528002574")
    sock.sendall(tosend)

def getCurrent(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 AT+SCURRENTPOWER=1\r\n"
    tosend=encrypt(msg,"9521314528002574")
    sock.sendall(tosend)
    data = sock.recv(1024)
    print decrypt(data, "9521314528002574")

def getVersion(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 AT+SV\r\n"
    tosend=encrypt(msg,"9521314528002574")
    sock.sendall(tosend)
    data = sock.recv(1024)
    print decrypt(data, "9521314528002574")


def discover():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', 7682))
    sock.sendto("HF", ("<broadcast>", 7682))
    while True:
        data, addr = sock.recvfrom(1024)
        print "Probe response: ", data



if len(sys.argv) != 3:
    print sys.argv[0], " [command] [ip address]"
    sys.exit(1)

if sys.argv[1] == "on":
    turnOn(sys.argv[2])
if sys.argv[1] == "off":
    turnOff(sys.argv[2])
if sys.argv[1] == "current":
    getCurrent(sys.argv[2])
if sys.argv[1] == "version":
    getVersion(sys.argv[2])
if sys.argv[1] == "discover":
    discover()




