Salt-SSH usage _shouldn't_ be different from the 'standard' _Salt Master_, _Salt Minion_ usage

The minimal config (`/etc/salt/roster`) file:
```
the.hostname.com:
  host: 192.168.1.2
  user: user
```

`salt-ssh` will upload `/etc/salt/pki/master/ssh/salt-ssh.rsa` to the `the.hostname.com` so that public key authentication
is used later on. Upon first connection, the `user` password will be required to provide in the prompt
```
Permission denied for host the.hostname.com, do you want to deploy the salt-ssh key? (password required):
[Y/n]                                                         
Password for user@the.hostname.com:   
```

Previous `roster` file is very limited, such config won't allow to execute any state that requires elevated privileges.

In order to fix this the `user` must belong to `sudo` group and have `NOPASSWD` setting in `sudoers` file. As of current:
`2019.2.2` version both settings are **required** 

# Thin dir
`salt-ssh` uploads some environmental data to the remote and places it under `thin_dir` (default: `/var/tmp` - contrary to `/tmp` from [doc](https://docs.saltstack.com/en/latest/topics/ssh/roster.html#ssh-roster)) 
It contains `salt-call` along with packaged custom modules, lowstate and grains.

# Log
Using `-l <log level>` doesn't provide logs from remote host, thus if some modules are missing on remote, user won't know it.  
This is somewhat consistent with Salt Master - Minion deployments where Salt Minion logs provide more details about issues during state execution

In oder to gather logs from remote:
```
the.hostname.com:
  host: 192.168.1.2
  user: user
  minion_opts:
    log_level: debug
    log_level_logfile: debug
    log_file: ../../salt-ssh.log
```
Putting absolute path as `log_file` doesn't allow to gather logs, this must be relative path
 
