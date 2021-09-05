# Virtual Function I/O
Set of technologies that allows to 'push' device(s) to virtual machine.  
The device is managed by the VM only, 'typical' use case for Linux hosts: Windows guest VM with GPU access.

Allows writing userspace drivers.

## GPU passthrough Debian setup
Ensure:
```
> egrep -q '^flags.*(svm|vmx)' /proc/cpuinfo && echo virtualization extensions available
virtualization extensions available
> aptitude install qemu-kvm
...
```
Enable [IOMMU (mapping of device address to main memory)](https://en.wikipedia.org/wiki/Input%E2%80%93output_memory_management_unit):
```
> cat /etc/default/grub.d/vfio.cfg
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
```
Find PCI port, using script that groups devices by their IOMMU groups
```
#!/bin/bash
shopt -s nullglob
for g in /sys/kernel/iommu_groups/*; do
    echo "IOMMU Group ${g##*/}:"
    for d in $g/devices/*; do
        echo -e "\t$(lspci -nns ${d##*/})"
    done;
done;
```
It may not be possible to 'push' single device to VM, normally whole IOMMU group is 'pushed'. 
This means that all devices belonging to such group won't be available on host.

```
> cat /usr/share/initramfs-tools/modules.d/vfio
vfio_pci ids=10df:1122,10de:1133,10de:1aaa,11de:bbbb
vfio_iommu_type1
> update-initramfs -u -k all
```

Disable any drivers that may take over device before VFIO (kernel)
```
> cat /etc/modprobe.d/nvidia.conf
softdep nouveau pre: vfio-pci 
softdep nvidia pre: vfio-pci 
softdep nvidia* pre: vfio-pci

> cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf
blacklist nouveau
options nouveau modeset=0
```
Reboot, and verify
```
> lspci -v
01:00.0 VGA compatible controller: NVIDIA ... [GeForce ... Rev. A] (rev ...) (prog-if 00 [VGA controller])
...
        Kernel driver in use: vfio-pci
...
```

Create VM, attach GPU, configure `evdev` so that same mouse is shared between host and guest. 

# References
1. https://www.kernel.org/doc/Documentation/vfio.txt
2. https://passthroughpo.st/gpu-debian/
3. https://passthroughpo.st/using-evdev-passthrough-seamless-vm-input/
4. https://mathiashueber.com/windows-virtual-machine-gpu-passthrough-ubuntu/
5. https://wiki.debian.org/VGAPassthrough