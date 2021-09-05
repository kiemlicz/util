# libvirt
## Requirements
Install with:
`aptitude install qemu-kvm libvirt-clients libvirt-daemon-system`

In order to permit user for vm management
```
adduser <youruser> libvirt
adduser <youruser> libvirt-qemu
```
## Configuration
Add storage pool
```
virsh -c qemu:///system pool-define-as $pool_name dir --target $location
```

# References
1. https://wiki.debian.org/KVM
2. https://libvirt.org/docs.html
3. http://rabexc.org/posts/how-to-get-started-with-libvirt-on