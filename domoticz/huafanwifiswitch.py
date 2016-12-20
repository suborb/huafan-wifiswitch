"""
<plugin key="huafanwifiswitch" name="HuaFan Wifi Switch" author="suborb" version="1.0.0" wikilink="http://github.com/suborb/huafan-wifiswitch" externallink="http://localhost/">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
    </params>
</plugin>

"""
import sys
sys.path.append("/usr/local/lib/python3.4/dist-packages/")
import Domoticz
from Crypto.Cipher import AES
import base64

isConnected = False


def onStart():
    if (len(Devices) == 0):
        Domoticz.Device(Name="Status",  Unit=1, Type=244,  Subtype=73, Switchtype=0).Create()
        Domoticz.Device(Name="Usage", Unit=2, Type=248, Subtype=1, Switchtype=0, Image=0, Options="").Create()

    Domoticz.Transport("TCP/IP", Parameters["Address"], "7681")
    Domoticz.Protocol("line")
    Domoticz.Connect()
    return True

def onConnect(Status, Description):
    global isConnected
    if (Status == 0):
        isConnected = True
        Domoticz.Log("Connected successfully to: " + Parameters["Address"])
        execCommand("AT+SCURRENTPOWER=1")
    else:
        isConnected = False
        Domoticz.Log("Failed to connect to: " + Parameters["Address"])

    return True

def onMessage(Data):
    decrypted = decrypt(Data, "9521314528002574")
    decrypted = str(decrypted,'utf-8')
    parts = decrypted.split()

    if parts[0] == 'S':
        if parts[2].startswith("+SNODE") == True:
            index = parts[2].index(",")
            result = parts[2][index+1]
            if result == '1':
                UpdateDevice(1, 1, '')
            if result == '2':
                UpdateDevice(1, 0, '')
        elif parts[2].startswith("+SCURRENTPOWER") == True:
            parts2 = parts[2].split(',')
            watts=int(parts2[2]) / 100.
            #Domoticz.Log("Power update for " + Parameters["Address"] + " is " + str(watts))
            UpdateDevice(2, 0,str(watts))
            # Update the status based on this message
            if parts2[1] == '1':
                UpdateDevice(1, 1, '')
            elif parts2[1] == '2':
                UpdateDevice(1, 0, '')
        else:
            print(decrypted)
    return True

def onCommand(Unit, Command, Level, Hue):
    Command = Command.strip()
    action, sep, params = Command.partition(' ')
    action = action.capitalize()

    if action == 'On':
        execCommand("AT+SOPEN=1")
    if action == 'Off':
        execCommand("AT+SCLOSE=1")
   
    return True

def onNotification(Data):
    Domoticz.Log("Notification: " + str(Data))
    return

def onHeartbeat():
    execCommand("AT+SCURRENTPOWER=1")
    return True

def onDisconnect():
    global isConnected
    isconnected = False
    return
   

def onStop():
    Domoticz.Log("onStop called")
    return True


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

def execCommand(cmd):
    msg="P 888888 " + cmd + "\r\n"
    tosend=str(encrypt(msg,"9521314528002574"),'utf-8')
    Domoticz.Send(tosend)
    return

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
