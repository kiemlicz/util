# ISO/OSI Layer 2
Data link access, responsible for access and data transfer through physical medium  
Defines the transport unit: _frame_ and mechanism of send/receive.

Consists of two components: Logical Link Control (LLC) and Media Access Control (MAC)

Layer 2 implementations: Ethernet, WiFi, Token Ring, PPP

## MAC
- divides the data into frames
- provides addressing
- provides medium access
- differs depending on layer 1

### Addressing
Non hierarchinal, flat, 6 Bytes. Address types:
 - unicast
 - multicast `01:...` (lsb of most significant byte eqal to 1)
 - broadcast `FF:FF:FF:FF:FF:FF`

First 3 Bytes denote NIC producent

### Carrier Sense Multiple Access with Collision Detection - CSMA/CD
Ethernet protocol governing data transmission.

#### Carrier Sense
Each host monitors the medium. If the medium is busy then no transmission happens.

#### Multiple Access
If the medium is free, wait IFG (_inter frame gap_) time and begin transmission. Between every two frames there is at least IFG idle time.
Since multiple hosts may detect that the medium is free, they may start transmission simultaneously causing collision.

#### Collision Detection
If the collision is detected, apply to all colliding hosts
1. finish sending preamble (if applies)  
1. send jam sequence (32 bits)  
1. stop sending  
1. backoff  
1. retry send

In Ethernet segment the collision can't occur after sending 64B

### Ethernet network segment size
In order to calculate Ethernet segment size, following assumptions are made:
1. the Ethernet frame cannot be send without guarantee that no collision occurs.
1. minimal frame size is 64B
1. time to send minimal frame is called the _time slot_
1. the time slot must be sufficiently long to: detect collision and send jam sequence in the maximum-sized network segment

Time to send minimal frame is 51.2 us in 10Mb/s Ethernet network  
Packet travels roughly 2/3 c time ~= 200 000 km/s  
In order to find maximum allowed segment size:
- assume that collision occurs at the farthest point
- the host at that point immediately detects collision and sends the jam sequence
- the jam sequence must reach the sender within slot time and within same time the sender must receive it:  
`51.2us == 2(propagation time) + jam sequence send time + jam sequence receive time`
Assume that `jam sequence send time` == `jam sequence receive time` == 9.6us (longer than sole jam sequence)  
The propagation time becomes: 16us and given propagation speed of 2/3 c the maximum theoretical size is 3.2km.  
In reality due to intermediate equipment it is less than 3.2km

## LLC
- retransmission
- gathering data from MAC
- error detection

## Frame 802.3
| preamble (8B) | destination address (6B) | source address (6B) | Type (2B) | Data (46B-1500B) | Frame Sequence Check (2B) |
|-|-|-|-|-|-|
|-|-|-|0800 - IPv4, 08100 - 802.1q|zero padded if less than 46B|CRC|

# References
