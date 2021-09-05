# IPsec
IP-IP tunnelling type.  
**Suite** of protocols for securing network communication.  
Uses orthogonal concepts

## Concept: AH vs ESP
Main L3 protocols, IP packet's `proto` field point to either AH (51) or ESP(50)

### AH (51)
Authentication only, doesn't provide encryption. Auth (hash-based) is computed using all IP header fields (but TTL and header checksum)

Notable headers:
- Security Parameter Index: 32bit identifier, used by recipient to fetch the security context associated with the packet
- Authentication Data: calculated hash value, mismatched hash value means the packet is discarded

Incompatible with NATs since IP addresses are used to compute the hash,
intermediate parties doing NAT don't know the secret key to recompute the hash.
Thus the receiving site drops the packets.

### ESP (50)
Provides encryption and flow identifier (Security Parameter Index - SPI) 

## Concept: Tunnel vs Transport
Informs what parts of IP packet to encrypt.
The 'implementation' difference: `next header` field in **AH** or **ESP** header.
| `next header` (symbolic name) | mode |
|-|-|
|`ip`| tunnel mode |
|`AH` or `ESP`| transport mode |

### Transport
Provides encryption or authentication (or both). 
The IP header is not encrypted.
The routing information is not modified (IP header is left unchanged).
The IP header determines the policy to be used for the packet.  
Typically, used for a host to host IPsec.

Example for AH mode
| IP header | AH header | TCP |

Typically, used to secure communication between hosts

### Tunnel
The entire IP packet is encapsulated.
Implication of that is following: the encapsulated source/destination addresses may be different than these in IP header (routing information is changed).

| IP header | AH header | IP header | TCP |

Typically used to secure communication between networks

## Concept: IKE vs manual
Mechanism of negotiating keys

### IKE
In Linux typically implemented via `pluto` or `charon` (part of StrongSwan userspace application)

Authenticates both VPN 'ends' to each other. 
IKE is encapsulated in UDP port 500.
IKE detects NAT and [switches to UDP port 4500 when NAT is found](https://tools.ietf.org/html/rfc3947#section-4).
IKA_SA is kept in userspace, other SA and SP are sent to kernel via netlink socket, the tunnel is considered "up".

### Manual
`charon` provides the IKE protocol to derive the key used for encryption or authentication. 
In order to do that manually, check: https://github.com/kiemlicz/util/blob/master/net/ipsec_functions#L4

## Concept: main mode vs aggressive
TODO

# Processing
Description of the IPsec processing on the Linux OS
![IPsec implementation](https://thermalcircle.de/lib/exe/fetch.php?media=linux:linux-ipsec-impl1.png)
After negotiating IKE_SA the SA and SP for actual VPN connection are negotiated and injected into kernel.
The IPsec processing uses XFRM framework (the part of kernel), it is "hooked" into packet flow (`xfrm` states), allows for various 'transforms':
![Packet flow](https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Netfilter-packet-flow.svg/2000px-Netfilter-packet-flow.svg.png)
There are actually three XFRM lookup calls (diagram shows only two). 
The use of either of them is determined by packet destination address:
- `dir in` input policy, selector for **already decrypted** packages
- `dir out` output policy, selector for packets to be encrypted
- `dir fwd` forward policy, selector for **already decrypted** packages with non-local destination

### `xfrm/socket lookup`
Multiple things happen here
1. ESP packets are matched against SAD (by {src IP, dst IP, SPI}). If matched then packed is passed to decode 
1. already decrypted packets are matched against SPD (`dir in` input policy), if the match is found then the packet is processed further, otherwise droppped 

### `xfrm decode`
Decrypt and decapsulate based on SA

### `xfrm encode`
Encrypt and encapsulate based on SA

### `xfrm fwd lookup`
Not shown in packet flow diagram. Relevant only for already decrypted packets.
Packets are matched against SPD (`dir fwd` forward policy, if the match is found then the packet is processed further (forwarded), otherwise droppped

### `xfrm lookup`
Checks SPD (`dir out` output policy), if match is found then the packet is moved to `xfrm encode`

## Security Policy Database (SPD)
What to encrypt, e.g, "all packets from 10.0.0.0/13 IPsec encrypt"  
`ip xfrm policy` dumps all policies. Typically, each IPsec connection will have at least three policies (in, out and fwd).  
A volatile DB (doesn't persist to disk)

## SAD
How to encrypt, or rather how to apply the security transformations  
`ip xfrm state` dumps all security associations, dumps the master key as well.  
A volatile DB (doesn't persist to disk)

## Packet flow
Sender side (simplified):
0. Send packet
1. `ip_route_output_flow()` check the routing information `ip route get <dst>`
2. `xfrm_lookup_route()` find IPsec SPDs (finds IPsec policy)
3. if no policy found: just send
4. if policy found, get `xfrm_state`. If the state is not yet established, drop UDP packet (TCP is not dropped) and establish the `xfrm_state` 

Received side (simplified):
0. Incoming packet
1. Decide if packet is for local process or not, if not then forward
2. if local and ESP packet then go into XFRM
3. find SA using SPI, validate keys, decrypt
4. submit decrypted IP packet back to IP stack

![Detailed flow](https://thermalcircle.de/lib/exe/fetch.php?media=linux:nf-hooks-xfrm-decode1.png)

# References
1. [One of the best IPsec descriptions](http://www.unixwiz.net/techtips/iguide-ipsec.html)
1. [IPsec in Linux kernel](https://www.youtube.com/watch?v=7oldcYljp4U) [Slides](https://libreswan.org/wiki/images/e/e0/Netdev-0x12-ipsec-flow.pdf)
1. [Great Linux IPsec implementation description](https://thermalcircle.de/doku.php?id=blog:linux:nftables_ipsec_packet_flow)
