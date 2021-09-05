# Init process
Main, first started process (typically id = 1, daemon)
Started by kernel, if start is unsuccessful, kernel panic occurs.
Multiple `init` implementations

## Upstart
## systemd
Maintains userspace applications
Each application is described in `unit` files. They use more declarative syntax instead of bash scripts.
Typically located in `/etc/systemd/system`
### unit file
Contains information nearly about anything: a service, socket, device, mount point, etc.
File name is used for control (via `systemctl`), though unit file can declare aliases (`Alias=`) that can be used too.

#### service declaration
Typically `systemd` controls one service but it is possible to spawn and control multiple instances of _service_.
In order to enable multi instance management:
 1. create service file with `@.service` suffix
 2. in unit file use `%i` placeholder for "some application instance"

# References