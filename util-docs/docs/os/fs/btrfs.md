# Setup
Preliminary:
 1. Kernel with btrfs support (located at `/lib/modules/$(uname -r)/kernel/fs/btrfs/btrfs.ko`)
 2. Userspace tools: `apt-get install btrfs-tools` (mainly for filesystem creation, conversion, etc.)

In order to create filesystem on device (even not partitioned one):
`mkfs.btrfs /dev/sdb /dev/sdc /dev/sdd`

# References
1. https://www.howtoforge.com/a-beginners-guide-to-btrfs
2. https://wiki.debian.org/Btrfs
3. http://marc.merlins.org/perso/btrfs/post_2014-05-04_Fixing-Btrfs-Filesystem-Full-Problems.html
4. https://btrfs.wiki.kernel.org/index.php/Balance_Filters