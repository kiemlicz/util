# Basics
TCP/UDP connection is identified by so called 5-tuple:  
`(protocol, source address, source port, destination address, destination port)`  
Protocol is set when `socket()` is called  
Source address and source port is set when `bind()` is called  
Destination address and destination prot is set when `connect()` is called (even for UDP)  

In order to bind to any address, user can specify address `0.0.0.0` or `::`. In practice it means: all IP addresses of all local interfaces. During the succeeding `connect()` call the OS will choose proper source IP based on destination address and contents of routing table.  
In order to bind to any ephemeral port, user can specify `port = 0`, then the OS will choose the port  
By default no two sockets can be bound to same `(source address, source port)`, e.g., if any socket is bound to `0.0.0.0:21`, then no other address can be bound to port 21

# Syscalls
| syscall | info |
|-|-|
|socket(domain, type, protocol)|returns socket file descriptor (fd)|
|bind(fd, *addr, addrlen)|bind to address, returns error code|
|listen(fd, backlog)|mark socket as passive (this is: as a socket accepting connections), backlog determines the maximum length to which the queue of pending connections for fd may grow|
|send()|adds the data to the send buffer, it doesn't necessarily mean that the data has been sent out. In case of UDP it is possible that the data is send immediately, but for TCP it is unlikely |

## Socket options
Socket behavior can be changed, moreover options meaning differ with every OS

### SO_REUSEADDR

Enabled prior to binding.
Theoretically `SO_REUSEADDR` has effect only on wildcard addresses and affects possibility of binding to 'taken' address.  

| SO_REUSEADDR | socketA | socketB | result (of socketB `bind()`) |
|-|-|-|-|
|true/false|`192.168.1.1:21`|`192.168.1.1:21`|EADDRINUSE|
|true/false|`192.168.1.1:21`|`10.0.0.1:21`|OK|
|false|`0.0.0.0:21`|`192.168.1.1:21`|EADDRINUSE|
|true|`0.0.0.0:21`|`192.168.1.1:21`|OK|
|true/false|`0.0.0.0:21`|`0.0.0.0:21`|EADDRINUSE|

Impact:
 1. For TCP sockets: the TCP socket after `close()` call, finally transitions to the `TIME_WAIT` (waiting for the data in socket buffers to be send). 
The amount of time the socket stays in this state is determined by _linger time_ (OS and socket level - `SO_LINGER` - configurable option). 
If `SO_REUSEADDR` is **not** set for such socket then closed TCP socket is still considered bound (up to _linger time_). 
However if `SO_REUSEADDR` is set, it is possible to bind to such (not-yet-fully) closed socket (without waiting _linger time_)
 2. For TCP sockets: it is possible that socket reusing address connects to the same destination address and port. Thus the 5-tuple is duplicated and `connect()` will fail with `EADDRINUSE`
 3. For UDP sockets: multiple multicast (one-to-many) sockets with `SO_REUSEADDR` may be bound to same combination of multicast address and port (same behavior like `SO_REUSEPORT`)
 
### SO_REUSEPORT

Allows arbitrary number of sockets to bind to exactly the same source address and port as long as all prior bound sockets also had `SO_REUSEPORT` set.
For Linux (>= 3.9): all sockets that want to share the same combination of address and port must belong to processes that share the same effective user ID. 

## Bind options

### INADDR_ANY
Equal to calling `bind` for address "0.0.0.0" (`sin_addr.s_addr`), which specifies all available interfaces.

# TCP socket states
![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Tcp_state_diagram_fixed.svg/796px-Tcp_state_diagram_fixed.svg.png)

**Backlog** states how many connections can be queued before handing over (via `accept` call) to the application. TCP three-way handshake has SYN RECEIVED (SYN received and SYN+ACK sent) intermediate state, which transits to ESTABLISHED after receiving the ACK from client. Thus backlog can be implemented in two ways:

1. The implementation uses a single queue, the size of which is determined by the backlog argument of the _listen_ syscall. When a SYN packet is received, it sends back a SYN/ACK packet and adds the connection to the queue. When the corresponding ACK is received, the connection changes its state to ESTABLISHED and becomes eligible for handover to the application. This means that the queue can contain connections in two different states: SYN RECEIVED and ESTABLISHED. Only connections in the latter state can be returned to the application by the _accept_ syscall. In this approach if the queue is full then any consecutive three-way handshake will be unsuccessful (client syn will be dropped). Not used in linux 
2. The implementation uses two queues, a SYN queue (or incomplete connection queue) and an accept queue (or complete connection queue). Connections in state SYN RECEIVED are added to the SYN queue and later moved to the accept queue when their state changes to ESTABLISHED, i.e. when the ACK packet in the 3-way handshake is received. As the name implies, the _accept_ call is then implemented simply to consume connections from the accept queue. In this case, the backlog argument of the listen syscall determines the size of the accept queue (second queue). Linux default.  
To set the max length of incomplete queue (first queue) use: `/proc/sys/net/ipv4/tcp_max_syn_backlog`. What happens when accept queue is full and client ACK arrives? Depends on `/proc/sys/net/ipv4/tcp_abort_on_overflow` it may clean the incomplete connection (drop)


# References
1. http://veithen.github.io/2014/01/01/how-tcp-backlog-works-in-linux.html
2. https://github.com/torvalds/linux/blob/master/net/ipv4/tcp_ipv4.c
3. https://stackoverflow.com/questions/14388706/socket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t