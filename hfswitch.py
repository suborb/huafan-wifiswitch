
import socket
from Crypto.Cipher import AES
import base64
import sys
import argparse


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

def setTime(host,time):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 AT+STIME=" + time + "\r\n"
    tosend=encrypt(msg,"9521314528002574")
    sock.sendall(tosend)
    data = sock.recv(1024)
    print decrypt(data, "9521314528002574")


def execCommand(host,command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 7681))
    msg="P 888888 " + command + "\r\n"
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


def main():
    parser = argparse.ArgumentParser(description='Control a HuaFan WifiSwitch.')
    parser.add_argument("--host", dest='host', help="Host/address of the switch")
    parser.add_argument("--time", dest='time', help="time to set")
    parser.add_argument("--raw", dest='raw', help="Raw command")
    parser.add_argument("command",  help="Command to run")

    args = parser.parse_args()

    if args.command == "discover":
        discover()

    if args.raw != None and args.command == "decode":
        print decrypt(args.raw, "9521314528002574")
	sys.exit(0)

    if args.host == None:
        parser.print_help()

    if args.command =="on":
        execCommand(args.host, "AT+SOPEN=1")
    if args.command =="off":
        execCommand(args.host, "AT+SCLOSE=1")
    if args.command =="current":
        execCommand(args.host, "AT+SCURRENTPOWER=1")
    if args.command =="version":
        execCommand(args.host, "AT+SV")
    if args.command =="gettime":
        execCommand(args.host, "AT+STIME?")
    if args.command == "getsignal":
        execCommand(args.host, "AT+SRSSI=1?")


    # Settime is overwritten seemingly
    if args.time != None and args.command == "settime":
        setTime(args.host, args.time)

    if args.raw != None and args.command == "raw":
        execCommand(args.host, args.raw)


main()

# Timer commands
#
# P 888888 AT+STIMETASK=1,01042303
# Task on Tuesday, 2303
# P 888888 AT+STIMETASK=1,02042303
# Task off Tuesday 2303
# P 888888 AT+STIMETASK=1,020C2303
# Task off Tuesday + Wednesday 2303 
# P 888888 AT+STIMETASK=1,00000000
# Delete task 
# 1,020C2303
# ^^^^^^^^^^
# ||||||time
# ||||dd           (bit set, bit=0 = sunday)
# ||st             (state, 02=off, 01=on)
# nr               (task number)




