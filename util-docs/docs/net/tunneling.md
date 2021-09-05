In Linux there are three types of tunneling (attaching network to network)  
Mind that tunnels introduce headers overhead which must be accounted for when setting the link MTU.

# IP in IP
IP packet encapsulated inside IP

# GRE
Very similar to IPIP but supports multicast

# Userland
Anything allowing to connect two networks that 'live' outside the kernel

# References
1. https://tldp.org/HOWTO/pdf/Adv-Routing-HOWTO.pdf
1. https://developers.redhat.com/blog/2019/05/17/an-introduction-to-linux-virtual-interfaces-tunnels/