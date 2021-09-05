# Basics
Normally packets received must have destination MAC address equal to NIC's MAC address.
Exceptions:
 1. Broadcast destination: `0xFFFFFFFFFFFF`
 2. Multicast destination: for IPv4 `0x01.....`, for IPv6 `0x3333....`

# Tcpdump
Tool based on _libpcap_ for packet capture.
Traffic dumping takes place at specific points in time:
* Incoming traffic: `wire -> NIC -> tcpdump -> netfilter/iptables -> application`
* Outgoing traffic: `application -> iptables -> tcpdump -> NIC -> wire`

## Dumping traffic with MAC of NIC
Dump local traffic using tcpdump:  
`tcpdump -i eth0 -w /tmp/outfile.pcap host 1.1.1.1`

Dump traffic on remote (eth0) host and visualize it locally with wireshark:  

1. Without access to `tcpdump` binary on remote
    ```
    mkfifo /tmp/dump
    ssh user@remote "sudo tcpdump -s0 -U -n -w - -i eth0 'not port 22'" > /tmp/dump
    wireshark -k -i <(cat /tmp/dump)
    ```
2. Having user access to `tcpdump` binary on remote, it is as simple as:  
    `ssh -C user@remote "tcpdump -i any -s0 -U -w - host 1.2.3.4" | wireshark -k -i -`  
   If `sudo` is available remotely, perform:  
   1. `groupadd pcap`
   2. `usermod -a -G pcap $USER`
   3. `chgrp pcap /usr/sbin/tcpdump`
   4. `chmod 750 /usr/sbin/tcpdump`
   5. `setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump`

## Dumping any traffic aka. sniffing

# References
1. https://www.wains.be/pub/networking/tcpdump_advanced_filters.txt
2. https://peternixon.net/news/2012/01/28/configure-tcpdump-work-non-root-user-opensuse-using-file-system-capabilities/