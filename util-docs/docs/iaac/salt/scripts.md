Means of interaction with Salt  
[@carsonoid](https://github.com/carsonoid) groups the scripts by their purpose.

### Action scripts
Interaction with _Salt Master_ or _Salt Minion_

#### salt
`salt '*' test.ping`  
salt runs on master, accepts the user command, applies them via salt-master process  
`(salt -> salt-master)    --transport-->    salt-minions`

#### salt-call
salt-call runs the execution modules directly, **doesn't require running salt-minion at all**, 
unless `--local` option is passed it still requires salt-master connection

#### salt-run
salt-run runs on the master, talks to the salt-master process, allows to run `runner` modules. `runner` modules allows to
orchestrate multi-minion installations

#### salt-ssh
Doesn't use Salt Minion process at all, requires only SSH daemon running.
Installs python binaries on the remote minion.  
It is much slower than using salt-minion
More detailed description of `salt-ssh` can be found [here](Salt-SSH.md)

#### salt-cloud
Runs on the master. Requires additional configuration of:  
  - cloud provider connection
  - image profiles (of the vm) 

Connects to desired cloud provider, allocates the resources, uses `salt-ssh` to provision image after its creation.

### Daemon scripts
Tools to extend access to salt

#### salt-api
Runs on the salt-master and communicates with salt-master process. Exposes multiple connectors and ACL.

Using curl, access API like so: `curl -sSk https://salt.local:9191/login -H 'Accept: application/x-yaml' -d username=saltuser -d password=saltpassword -d eauth=auto`

#### salt-proxy
Pretends to be salt-minion, allows provisioning of the devices that cannot run salt-minion or cannot be connected via SSH.
Salt-master is not aware of the proxy.

#### salt-syndic
Runs on multiple salt-masters and proxies traffic from multiple masters to one desired (uber) salt-master. 

### Utility scripts
Salt itself management 

#### salt-key
Runs on salt-master, manages minion keys.

List all of the keys: `salt-key -L`  
Accept key:  `salt-key -a minion_id`

#### salt-cp
Copy files from salt-master to salt-minion (other way around as well)

#### spm
Salt Package Manager, standarization over multiple salt formulas. Currently adding formulas requires changes in _Salt Master_ configuration.
With spm this is no longer necessary.

#### salt-extend
Boilerplate generator for custom modules.

#### salt-unity
Wrapper over any other script: `salt-unity key -L`.  
This is useful for tools that require listing allowed user commands (like sudoers file)
