# Compilation
# Upgrade
After installing new kernel dependent ("external") modules needs to be rebuild.  
In Debian family _dkms_ is responsible for detecting dependent modules and rebuilding them.  
To find which modules needs to be rebuild after upgrade, use: `dkms status`
## Troubleshooting
`dkms` may yield:
```
Error! Could not locate dkms.conf file.
File: does not exist.
```
It means that your installation contains old kernel modules, not properly removed/upgraded.  
Kernel modules are usually located in `/var/lib/dkms/` (or in `/usr/src`).  
List them:
`for i in /var/lib/dkms/*/[^k]*/source; do [ -e "$i" ] || echo "$i";done`  
Remove those that are no longer installed (old ones):
`rm -rf /var/lib/dkms/something/old_version`

# References
1. https://forums.virtualbox.org/viewtopic.php?f=7&t=76493#
2. https://wiki.debian.org/KernelDKMS