# Unattended system provisioning
Unattended installation comprises of two phases:
1. Installation of OS itself with automatic answers
2. Provisioning of installed OS (application installation, configuration etc.)

## OS installation
Automated OS installation process utilizes PXE boot.
1. The UEFI/BIOS sends DHCP discover request
2. The DHCP offer must contain `TFTP Server Name` (option 66) and `Filename` (option 67)
3. BIOS/UEFI downloads the loader from TFTP server and runs it

The process looks like (BIOS example) this:  
![](https://icefyresan.files.wordpress.com/2014/12/pxe.jpg)

PXE booting relies on platform firmware, its configuration files are different for BIOS and its successor UEFI.

The available UEFI loaders (for BIOS just send the `pxelinux.0` file):
1. Syslinux. Can download images via TFTP, contains many bugs, e.g. the TFTP download of linux image may take long time and syslinux will
terminate the download process with timeout. This breaks the whole process
2. GRUB. This must be pre-build grub image with PXE support that will continue to download the initrd/image from servers.
3. iPXE. The de-facto standard, open-source and most robust solution. Can download initrd/image from the HTTP servers thus 
making it the most reliable.

### [BIOS](https://en.wikipedia.org/wiki/BIOS)
Hardware initialization in not exactly standarized manner (as reverse engineered from IBM first implementation).  
After POST boots by reading and executing first sector on hard disk. 
Booting runs in 16-bit processor mode and has only 1MB of space to execute in. Has problems with parallel device initialization. 
Can boot only from hard disks of size less than 2.1TB  
Uses MBR partitioning scheme

### UEFI
Has no limitations of BIOS, standarized (by Intel).  
Specifies following servies available for OS and OS loader:  

|System table|
|----|
|Boot time services|
|Run time services|
|Console|
|Additional tables|

Boots by loading EFI program files.  
Uses GPT partitioning scheme

# References
 1. https://www.debian.org/releases/stretch/example-preseed.txt
 2. https://wikitech.wikimedia.org/wiki/PartMan
 3. https://wiki.debian.org/DebianInstaller/Preseed
 4. https://www.debian.org/releases/stable/amd64/ch03s06.html.en#UEFI
 5. http://fai-project.org/fai-guide/
 6. https://www.youtube.com/watch?v=bNL1pd-rwCU
 7. https://www.howtogeek.com/56958/htg-explains-how-uefi-will-replace-the-bios/
 8. https://superuser.com/questions/496026/what-is-the-difference-in-boot-with-bios-and-boot-with-uefi