# Basics
| IP | Meaning | Usual name |
|-----------|---------| --------|
| 127.0.0.1 | Loopback address, primarly for debugging and connecting to local servers | localhost |
| 127.0.1.1 | Mapping of hostname to IP in case network is not available. For systems with permanent IP, permanent IP should be used instead of 127.0.1.1 | `$(hostname)` |

To get/set system name use: `hostname`  
To get DNS domain name use: `dnsdomainname`

To set DNS domain name (or rather _FQDN_: Fully Qualified Domain Name, which consists of hostname concatenated with domain name) use fqdn aliases for 127.0.1.1 in `/etc/hosts` (e.g. `127.0.1.1 myhostname.my.domain.com myhostname`). Setting DNS domain may cause troubles in case of multi-interface nodes.

# Debian-based OSes net config
Static network configuration in `/etc/network/interfaces`:
```
auto eth0
iface eth0 inet static
    address 192.0.2.7
    netmask 255.255.255.0
    gateway 192.0.2.254
```
DNS servers IP addresses reside in `/etc/resolv.conf`

## Usage of NetworkManager
NetworkManager can read `/etc/network/interfaces` file if configured to do so via `/etc/NetworkManager/NetworkManager.conf`
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
# References
 1. [Debian network configuration](https://wiki.debian.org/NetworkConfiguration)

