# Configuration
Written in YAML files, located in `/etc/salt/master` and `/etc/salt/master.d/`  
Master configuration: `/etc/salt/master`  
Master configuration overrides: `/etc/salt/master.d/myoverrides.conf`  
Minion configuration: `/etc/salt/minion`  
Minion configuration overrides: `/etc/salt/minion.d/myoverrides.conf`  
Overrides **require** `.conf` suffix, otherwise they are not included and nothing is logged.  

## States
Defined using `*.sls` files, located in state directories listed in `file_roots` configuration option (`/srv/salt/` by default).  
The state directories are also called _State Tree_  
Example of state file contents:
```
funny_user_setup:                 # state ID
  user.present:                   # <state module>.<function>
    - name: cool_guy              # <function's> arguments
    - fullname: Cool Guy Jr
    - shell: /bin/bash
    - home: /home/cool_guy
```
Given the above `file_roots` configuration this state file must be located in `/srv/salt/the_state.sls` or `/srv/salt/the_state/init.sls`, 
(the `init.sls` is treated as parent directory).  
The sls filename cannot contain dots (other than suffix `.sls`). Filename with dots is expanded by salt as directories, e.g.,
`the_state.something.sls` will be understood as `/srv/salt/the_state/something.sls`.  
When both `/srv/salt/the_state.sls` or `/srv/salt/the_state/init.sls` exist, the `the_state/init.sls` is ignored.   
By default the sls file represents python dictionaries, lists, strings and numbers only.

Salt also requires special file to exist in top level of _State Tree_. This special file is responsible for matching states to actual machines.
It is called `top.sls`, example:
```
base:
  'machine':
    - the_state
```
For more information about Top File structure and state definition refer to [Targeting and Top file](https://github.com/kiemlicz/util/wiki/Salt-Master#targeting-and-top-file)

### saltenv
`file_roots` configuration contains environment specification. In order to specify multiple environments list them along with their directories containing states:
```
file_roots:
  base:
    - /srv/salt/base
  dev:
    - /srv/salt/dev
```
It is possible to specify directories multiple times in order to 'reuse' some states from other environments:
```
file_roots:
  base:
    - /srv/salt/base
  dev:
    - /srv/salt/dev
    - /srv/salt/base
```

### Custom states
In order to create your own states, put them in `_states` under _State Tree_ root. This directory is configured to be synchronized
to minions upon `state.highstate` or `saltutil.sync_all` calls.

## Pillar
Defined in similar way as state files, located in directories listed in `pillar_roots` configuration option.
There is no enforced pillar data syntax, given default renderer the pillar must be just provided as YAML file.  
Example pillar data file:
```
some_user_data:
  mail: cool_guy@o2.io
  home_dir: /home/cool_guy
```
The `top.sls` file is also expected to exist in `pillar_roots` top directory.

### Custom pillar
Documentation refers to custom pillars as [external pillars](https://docs.saltstack.com/en/latest/topics/development/external_pillars.html).  
It is possible to extend Pillar subsystem to fetch data from arbitrary sources. The requirement is to implement: 
```
def ext_pillar( minion_id, pillar, *args, **kwargs ):
    ...
    
    return pillar_dict 
```
The external pillar must be configured in _Salt Master_ configuration first.
Some already existing custom pillars deserve special mentions.

#### git_pillar

#### file_tree
`ext pillar: file_tree`
File becomes the value of key  
Under the `root_dir` you must have either `hosts/minion_id` folder or `nodegroups/nodegroup` folder  
Data is available to matching hosts.  
Example configuration:  
```
ext_pillar:
  - file_tree:
      root_dir: /path/to/root/directory
      keep_newline:
        - files/testdir/*
```

#### gpg renderer
The pillar values can be encrypted using GPG.  
The keypair (without passphrase) must be either [setup](https://docs.saltstack.com/en/latest/ref/renderers/all/salt.renderers.gpg.html#setup) or [imported](https://github.com/kiemlicz/util/blob/master/sec/gpg_functions#L23) beforehand on the master node (or on masterless node).
It is possible to change default location of gpgkeys using: `gpg_keydir` configuration option.  
To create encrypted secret: `cat secret_file | gpg --armor --trust-model always -r pillargpg --encrypt --homedir ~/somewhere/the/keys`

## Dunder dictionaries
Some of the _Salt_ modules are 'wrapped' within special _dunder_ dictionaries. 
These special dictionaries provide access to _Salt_ **different** modules.

| Dictionary name | Available in | Information |
|-----------------|--------------|-------------|
| \_\_opts\_\_ | Loader modules | configuration file contents |
| \_\_salt\_\_ | Execution, State, Returner, Runner, SDB modules | **execution** modules |
| \_\_grains\_\_ | Execution, State, Returner, External Pillar modules | minion grains data |
| \_\_pillar\_\_ | Execution, State, Returner modules | pillar data |
| \_\_context\_\_ | Execution, State modules | all-purpose dict, that exists during all state runs |

### Using dunder dictionaries
#### Jinja2+YAML
Double underscores are omitted.
```
apache:
  pkg.installed:
    - name: {{ salt['pillar.get']('pkgs:apache', 'httpd') }}
```
  
```
{% for mnt in salt['cmd.run']('ls /dev/data/moose*').split() %}
/mnt/moose{{ mnt[-1] }}:
  mount.mounted:
    - device: {{ mnt }}
    - fstype: xfs
    - mkmnt: True
{% endfor %}
```
#### py
```
#!py

def run():
  states = {}
  swaps = __salt__['mount.swaps']()
  for swap, dev in swaps.items():
    states["kubeadm_disable_swap_{}".format(swap)] = {
      'module.run': [
        { 'mount.swapoff': [
          { 'name': swap },
        ]},
        { 'require_in': [
          { 'pkg': "kubeadm" }
          ]}
      ]
    }
  return states
```

## Fileserver
All of the above configuration samples assumed filesystem to be used as primary `sls` storage. 
Actually [fileserver is also a _Salt_ module](https://docs.saltstack.com/en/latest/ref/file_server/all/index.html).
Thus it is possible to create your own (place it in `_fileserver` directory under _State Tree_ root).
In order to enable different fileserver, switch them on in master configuration:
```
fileserver_backend:
  - roots
```
It is possible to specify multiple backends, they are merged together. The `sls` files that are same within backends
are taken in the order of their definition (`fileserver_backend` is a list after all).  

Example:
```
fileserver_backend:
  - roots
  - gitfs
```
If the `top.sls` file exists in both _gitfs_ and _roots_ top directories then the `roots` one will be used.

### gitfs
Enabled with:
```
fileserver_backend:
  - gitfs
```
Allows to pull state and pillar definitions from git repositories.

## Reactor
Part of the _Salt_, that starts different actions upon fired events. The configuration contains the list of handled events 
with different `sls` files run as a reaction.
```
reactor:
  - 'salt/job/*/ret/*':
    - salt://do_something_after_job.sls
    - /full/path/to/file.sls
```
By default this is configured in `/etc/salt/master` and `/etc/salt/master.d/reactor.conf`.  
Reactions can be specified using `/full/path/notation` or relative to _State Tree_: `salt://`

## Thorium

## Cloud

# Extending Salt
It is very easy to create your own _Salt_ modules or even alter existing ones. All of the module changes must be synchronized
to minions prior to use (this happens automatically only for `state.highstate` call). By default, extensions must be placed in directories in _State Tree_
root, following naming convention: `_<module_type>`.  
It is also possible to define custom extensions in different places, given proper `extension_modules` configuration.
Anything from [salt module](https://docs.saltstack.com/en/latest/ref/index.html) can be customized.

# [Salt SSH](https://docs.saltstack.com/en/latest/topics/ssh/)
No software needs to be installed on managed host, on the Salt Master side: `salt-ssh` package is required.  
Configure `/etc/salt/roster` file with remote host details, the working roster file:
```
minion:
  host: minion.local
  user: dev
  passwd: password  # required even if keys are used 
  sudo: true  
  tty: true
  minion_opts:
    log_level: debug
    log_level_logfile: debug
    log_file: ../../salt-ssh.log  # nice trick from https://twitter.com/SaltTips/status/1146306964026253312
```
The remote host must have at least `python-minimal` installed, the `passwd` is always mandatory (since on the remote the `sudo` is required)
Read more in [Salt-SSH](Salt-SSH.md)