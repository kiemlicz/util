# Implementations
## OpenSSH
Client configurations sourcing order (first obtained value is used):

1. User options 
2. `~/.ssh/config`
3. `/etc/ssh/ssh_config`

Debian-based OSes send `LANG` and `LC_*` variables over SSH (this is implemetation feature). If the server is configured to receive them (`AcceptEnv` option in _OpenSSH_) then locale must exist on the server-side (must be generated).

If the session hangs e.g. server breaks in order to release client use sequence: `Enter`, `~`, `.`

Execute local script on remote machine:  
`ssh user@remote 'bash -s' < ./local.script.sh`

Execute local script on remote machine and pass variables:  
`ssh user@remote VAR1="something" VAR2="something2" 'bash -s' < ./local.script.sh`

If the script requires `sudo` privileges simply replace `'bash -s'` with `'sudo bash -s'` but if the script also accepts variables then `sudo` must be invoked with `'-E'` flag: `'sudo -E bash -s'`. Otherwise variables wouldn't get passed to shell