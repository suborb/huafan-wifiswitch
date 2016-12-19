# Huafan Wifi Switch

This is a cheap wifi switch controlled by an esp8266. By default it works via two servers located in China. These servers have complete control over the switch so if suspicious I'd recommend firewalling off the plugs.

Example auction for them: http://www.ebay.co.uk/itm/Smart-WiFi-Wireless-Remote-Control-UK-Plug-Socket-Switch-Power-Mobile-Phone-App-/272277763047 (I didn't use this seller)

## The script

hfswitch.py allows the controlling of a switch and additionally allows usage statistics to me posted back to domoticz. For usage to work, the script should be run periodically.

## Servers the firmware contacts:

121.42.46.59 port 2110 and 5110. This is the main control host. Initially port 5110 is used, and then fails back to 2100. This runs a slightly different protocol to local usage.

115.29.202.58 port 8000. The switch talks to one of the servers under this domain and regularly issues a HTTP ping.


## Discovery

Plugs can be discovered with a UDP broadcast message targetted at port 7682.

Content of the broadcast message is:

```
HF
```

Response will be received of the format:

```
<model name>,<state>,<IP address>,<Mac address>
```

for example:

```
HF-W0B,2,192.168.4.1,00-00-00-00-00-00
```


## Controlling Protocol

The switch accepts a TCP connection on port 7681. The protocol is fairly simple, but is obfuscated using AES. The encryption key is "9521314528002574" and the IV is "4528453102574529".


## Turning the Switch on

### Command
```
P 888888 AT+SOPEN=1\r\n
```
### Response

```
S 000000000000 +SNODE:#1,1
```
Where 000000000000 is the mac address and the final 1 is the state of the switch.

## Turning the Switch off

### Command
```
P 888888 AT+SCLOSE=1\r\n
```
### Response

```
S 000000000000 +SNODE:#1,2
```
Where 000000000000 is the mac address and the final 2 is the state of the switch.

## Reading the power state

### Command
```
P 888888 AT+SCURRENTPOWER=1\r\n
```
### Response

```
S 000000000000 +SCURRENTPOWER:#1,1,WWWWWW,AAAAA
```

Where 000000000000 is the mac address and the final 2 is the state of the switch.

W is the wattage measured in 0.01W. A is the current in 0.0001A


## Switching between AP and Client mode

### Switch to standalone mode (AP)

```
P 888888 AT+SAPSTA=1
```

### Switch to station mode

```
P 888888 AT+SAPSTA=0
```

## Joining a network

From inspection, the appropriate command is:

```
P 888888 AT+SSSIDINFO=[SSID Length],[SSID],[Auth mode],[password]
```

Where [Auth mode] is one of the following values:

* AuthModeOpen = 0;
* AuthModeWPA = 3;
* AuthModeWPAPSK = 4;
* AuthModeWPA2 = 6;
* AuthModeWPA2PSK = 7;
* AuthModeWPA1WPA2 = 8;
* AuthModeWPA1PSKWPA2PSK = 9;

Response is:

```
S 000000000000 +SSSIDINFO:OK
```

Where 000000000000 is the mac address of the switch.
