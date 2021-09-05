Low power, long range, wide-area network (LPWAN network category)

Uses radio frequencies:
- 433 MHz
- 868 MHz Europe
- 915 MHz Australia, North America
- 867 MHz India
- 923 MHz Asia

Range: According to spec claims: 15km, according to wikipedia for rural areas ~10km, depends on obstacles.  
Data rates: 0.3 kbps - 50kbps

# Topology 
Star of stars (extended star)  
`Node (end device) -<LORA>- Gateway -<IP connection>- Network Server (Cloud) -<IP connection>- Application Server`  
Bi-directional communication, multicast support.
More than one gateway can relay the end device traffic (network server handles the redundancy).

## End device
Sends small amounts of data, infrequently over long distances.

## Gateway
Receives packets from Lora network and forwards it to the Network Server

## Network server
Removes the optional redundancy, chooses most appropriate gateway to send the acknowedgements. 
Handles the security (decrypts the packet) and end device activation. 
The network servers may instruct the gateways to change end devices' data rates to conserve power (ADR).

## Application server
Consumes end device data (decrypts as well). Sends data to end devices

# Physical Layer
The term: LoRa, per se defines the physical layer.  
Proprietary protocol derived from [CSS](https://en.wikipedia.org/wiki/Chirp_spread_spectrum).
Can be compared to ISO/OSI L1

# Communication Layer
Described by the LoRaWAN protocol.  
Hard to compare with any ISO/OSI layer since it descibes multiple network components.
![](http://www.techplayon.com/wp-content/uploads/2018/10/LoRa-Call2-730x342.png)

For end device to communicate with application, the registration within Network server is requried (this process is actually called "Activation").
To use raw LoRa no registration is required. Activation is granted based on Device EUI.  
Two activation methods exist

## Over The Air Authentication (OTAA)
From network obtain Application EUI and Application Key.
The end device joins the network using Application EUI, Application Key and Device EUI
The underlying network and application session key is auto-generated.

## Authentication By Personalization (ABP) 
The end device joins the network using manually pre-configured network session key, application session key and Device EUI

LoRaWAN defines different endpoint classes for different application needs

## Class A
Initiated by end device. Asynchronous: if the device has data to send: it sends. 
During that transmission, windows for downlink transmission (from the server) are added.
No requirements for wake-ups, device can behave however it wants.
Downlink can only follow uplink.

## Class B
Class A + end device opens scheduled downlink slots. This allows deterministic communication to the device.

## Class C
Class A + end device always open for downlink requests. This allows servers to initated communication to the device at any time.

## Security

# References
1. https://en.wikipedia.org/wiki/LoRa
1. https://docs.pycom.io/firmwareapi/pycom/network/lora/
1. https://docs.pycom.io/gettingstarted/registration/lora/
1. https://docs.pycom.io/tutorials/networks/lora/
1. https://lora-alliance.org/about-lorawan/
1. https://www.hindawi.com/journals/wcmc/2017/6590713/
1. https://www.thethingsindustries.com/news/what-lorawan-network-server/
1. https://www.chirpstack.io/project/architecture/