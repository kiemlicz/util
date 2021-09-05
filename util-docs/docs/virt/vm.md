# Virtualization

Requires running VM Monitor (Hypervisor) on the host, bare-metal machine. Coordinates host machine resource sharing.

## Types of Hypervisors
### Type1
### Type2

# Benefits
 - cheaper than bare-metal
 - isolation (guest OS is fully isolated from host and other guest OSes)
 - 'easy' migration
 - HA

# Drawbacks
 - performance overhead
 - sometimes host performs overprovisioning, which can cause serious performance degradation
 - Hypervisor is a single point of failure
 - extra management