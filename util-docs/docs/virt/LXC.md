Container's filesystem root location: `/var/lib/lxc/<container name>`  
Container creation scripts/templates for given distro: `/usr/share/lxc/templates`

To verify if LXC is supported on current OS/kernel run: `lxc-checkconfig`

Debian may have some issues with memory control via cgroups.  
Check kernel support: `cat /boot/config-$(uname -r) | grep CONFIG_MEMCG`  
If output contains both `CONFIG_MEMCG=y` and `CONFIG_MEMCG_DISABLED=y` means that memory cgroups must be explicitly enabled by kernel parameter (`cgroup_enable=memory`)

### Networking
Described in configuration file `lxc-create -f <config_file>`  
Create bridge interface on host OS and link to container:
```
lxc.network.type = veth
lxc.network.flags = up
lxc.network.link = br0

lxc.network.type = veth
lxc.network.flags = up
lxc.network.link = br1

lxc.network.type = empty
```
For "isolated" bridge interface for containers, configure `lxc-net`.  
Refer to [4](#References)

# References
 1. https://wiki.debian.org/LXC
 2. https://www.stgraber.org/2013/12/20/lxc-1-0-blog-post-series/
 3. https://www.flockport.com/guides/
 4. https://wiki.debian.org/LXC/SimpleBridge
 5. http://man7.org/linux/man-pages/man5/lxc.container.conf.5.html
 6. https://wiki.debian.org/BridgeNetworkConnections