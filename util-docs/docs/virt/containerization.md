# Containerization
Often seen as na advancement from `chroot` technique. For given process and its children `chroot` creates the filesystem 'isolation' only.

Containers provide more: process resources are isolated via kernel namespaces and resource usage is controlled via cgroups.  
Both the host and container share **the same kernel**.  
The "container" is not a in-kernel term. 
The closest definition: namespaces + cgroups = containers.

## Concepts
Following **linux kernel** concepts are the building blocks of containers

### Namespaces
Wrapper over global system resources.  
For all processes within the namespace makes the system resources appear like isolated (dedicated) instance.  
Changes to the global resource are visible to other processes that are members of the namespace, but are invisible to other processes.

By default linux provides following namespaces

| namespace | isolates |
|-|-|
| `Cgroup` | Cgroup root directory. Processes inside this namespace are only able to view paths relative to their namespace root |
| `IPC` | System V IPC, POSIX message queues |
| `Network` | Network devices, **ports**, etc. |
| `Mount` | Mount points |
| `PID` | Process IDs |
| `User` | User and group IDs |
| `UTS` | Hostname and [NIS](https://en.wikipedia.org/wiki/Network_Information_Service) domain |

Each namespace is assigned unique _inode_ number:
```
> ls /proc/7320/ns -al
dr-x--x--x 2 thedude thedude 0 May 20 20:19 .
dr-xr-xr-x 9 thedude thedude 0 May 20 19:29 ..
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 cgroup -> cgroup:[4076531835]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 ipc -> ipc:[4026537839]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 mnt -> mnt:[4026537840]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 net -> net:[4026537969]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 pid -> pid:[4026537836]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 user -> user:[4026731837]
lrwxrwxrwx 1 thedude thedude 0 May 20 20:19 uts -> uts:[4026571838]
```

#### userspace tools
`lsns`

### Control groups
Usually referred as cgroups. 
Linux feature that organises processes into hierarchical groups whose usage of various types of resources
can be limited and monitored 

### Union file systems
TODO

## Benefits
 - faster than full VM (doesn't require running hypervisor) 
 - easier to provision (doesn't require full VM setup)
 - cheaper
 - better resource utilization
 - easier to scale 

## Solutions
- [Docker](Docker)
- [LXC](LXC)

# References
 1. Modern Linux Administration - Sam R. Alapati
