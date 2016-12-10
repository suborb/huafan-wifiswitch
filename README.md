# Huafan Wifi Switch

This is a cheap wifi switch controlled by an esp8266. By default it works via two servers located in China. These servers have complete control over the switch so if suspicious I'd recommend firewalling off the plugs.

Firmware servers:

121.42.46.59 port 2110 and 5110. This is the main control host. The protocol between the plug and server is different to that described here, but uses the same AES characteristics.

iotbucket.com the switch talks to one of the servers under this domain and regularly issues a HTTP ping.

Code will come later, but the information here is enough to control a switch.


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

There are many commands available, the following are the most useful.

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
S 000000000000 +SCURRENTPOWER:#1,1,000000,00000
```

Where 000000000000 is the mac address and the final 2 is the state of the switch.


