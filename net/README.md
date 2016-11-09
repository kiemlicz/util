#Basics
Networking tools&notes of any kind

##General information
Debian based systems keep static network configuration in `/etc/network/interfaces`:
```
auto eth0
iface eth0 inet static
    address 192.0.2.7
    netmask 255.255.255.0
    gateway 192.0.2.254
```
DNS servers IP addresses reside in `/etc/resolv.conf`

###Usage of NetworkManager
NetworkManager can read `/etc/network/interfaces` file if configured to do so 
via `/etc/NetworkManager/NetworkManager.conf`
```
[ifupdown]
managed=true
```
To disable NetworkManager for given interface:
```
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=true

#this section allows network manager to stop managing specified interface
[keyfile]
unmanaged-devices=mac:aa:bb:cc:dd:ee:ff
```
#References
 1. [Debian network configuration](https://wiki.debian.org/NetworkConfiguration)

#Table of contents
Further networking operations:

 1.[TCPDUMP](sniff/README.md) 
