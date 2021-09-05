The routing table lists remote destinations (subnets) with the address of next-hop known to be closer to destination.  
On Linux hosts the routing table decides whether the packet should be forwarded or processed locally.  
Traditionally the Linux packet forwarding selects the route based on packet's destination IP.  
In order to enable forwarding to non-local destination: `sysctl -w net.ipv4.ip_forward=1`

## Routing table
`ip route show` will display _main_ routing table. Example output:
```
root@vm1:~# ip r s
default via 192.168.1.1 dev ens3 
10.244.0.0/24 dev cni0 proto kernel scope link src 10.244.0.1 
10.244.1.0/24 via 10.244.1.0 dev flannel.1 onlink 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown 
192.168.1.0/24 dev ens3 proto kernel scope link src 192.168.1.106 
```
Dissection:
`default` equals to `0.0.0.0/0`  
`dev <interface>` denotes to which interface given route is pinned  
`via <IP>` next hop, may depend on route type
`src <IP>` source address to prefer when using route  
`proto` how the route was installed

|proto|info|
|-|-|
|`redirect`|installed due to ICMP redirect|
|`kernel`|installed by the kernel during autoconfiguration|
|`boot`|installed during the bootup sequence|
|`static`|installed by administrator|
|`ra`|installed by Router Discovery Protocol|

`scope` determines how _valid_ given address is, if not present then `global` is assumed

|scope|info|
|-|-|
|`global`|valid everywhere|
|`site`|valid only within given site (IPv6)|
|`link`|valid only for given device|
|`host`|valid only within host, not routable|

## Routing policy
It is possible to route packet not only based on destination IP, but rather using some additional information, e.g. source address, protocol or packet size.  
In order to do that following kernel options must be enabled (`y`)
```
> cat /boot/config-$(uname -r) | grep CONFIG_IP_ADVANCED_ROUTER
CONFIG_IP_ADVANCED_ROUTER=y
> cat /boot/config-$(uname -r) | grep CONFIG_XFRM
CONFIG_XFRM=y
```
_Policies_ can route **selectively** traffic using different paths.  
_Policy_ is picked before routing decision.  
_Policy_ can determine which routing table to use (it is possible to have multiple routing tables).

### RPDB
Different routing tables are picked based on defined selector.  
`ip rule list` shows which route table will be used for particular set of information  
```
> ip rule list
> #default output
0:      from all lookup local 
32766:  from all lookup main 
32767:  from all lookup default 

> #other host
> ip rule list
0:      from all lookup local 
9:      from all fwmark 0x2 lookup o2 
10:     from all fwmark 0x1 lookup o1 
220:    from all lookup 220 
32766:  from all lookup main 
32767:  from all lookup default 
```

Dissection:
`0:` - first column shows entry priority. Lower the number, higher the priority  
`from all` - **the selector** part: any packet in this case  
`from all fwmark 0x1` - **the selector** part: any packet with iptables `mark` 0x1  
`lookup tablename` - **the action** part: use `tablename` routing table

Rules are scanned starting from the lowest number, selector is applied to {src address, dst address, in interface, tos, fwmark} 

in order to add routing table to the RPDB (Routing Policy Database):
`echo "100     o1" >> /etc/iproute2/rt_tables`

Display routing table entries: `ip r s t tablename`

## Debugging
`ip route get 1.2.3.4` will display which route will be used for particular destination.  
`ip route get 1.2.3.4 mark 1` will display which route will be used for particular destination with some additional information (`mark` in this example).  

# References
1. https://tldp.org/HOWTO/pdf/Adv-Routing-HOWTO.pdf
1. https://silo.tips/download/advanced-routing-scenarios-policy-based-routing-concepts-and-linux-implementatio
1. https://upload.wikimedia.org/wikipedia/commons/3/37/Netfilter-packet-flow.svg
1. http://linux-ip.net/html/tools-ip-rule.html
1. [Available IP rules](https://manpages.debian.org/buster/iproute2/ip-rule.8.en.html)
