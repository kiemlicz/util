Main (debian) doc:
https://wiki.debian.org/NetworkConfiguration

Static network interface address configuration:

auto eth0
iface eth0 inet static
    address 192.0.2.7
    netmask 255.255.255.0
    gateway 192.0.2.254

DNS servers reside in:
/etc/resolv.conf

Usage of network manager:
NetworkManager can read /etc/network/interfaces file if configured to do so (/etc/NetworkManager/NetworkManager.conf):

  [ifupdown]
  managed=true

You can disable NetworkManager for given interface like so:
$ cat /etc/NetworkManager/NetworkManager.conf
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=true

#this section allows network manager to stop managing specified interface
[keyfile]
unmanaged-devices=mac:aa:bb:cc:dd:ee:ff
