Responsible for managing the minions.  
Provides the states and the pillar data.
States are send and rendered on minions, pillars are send and cached on minions.  
In order to match states and pillar data that should be send to given minions the [targeting](https://docs.saltstack.com/en/latest/topics/targeting/) is used. 

Similarly, to _Salt Minion_ the _Salt Master_ also has ID, which is equal to hostname with `_master` suffix.
It is also possible to override this setting in the master config: `id` 

## Targeting and Top file
Targeting is specifying which minions should execute given state as well as contain given pillar data.

Typically targeting is contained in [`top.sls`](https://docs.saltstack.com/en/latest/ref/states/top.html) file.  
```
base:              # environment 
  'minion_id':     # target
    - some_state   # states
```
`top.sls` consists of three parts:
 - environment (_saltenv_) - main one, contains targets
 - target - contains states
 - states

### Environments aka saltenv
Most often used to isolate operations within different... environments, e.g., `dev`, `test`, `prod`.   
Requires [additional configuration](https://github.com/kiemlicz/util/wiki/Salt-configuration#saltenv)  
Helps to:
 - Group minions by their role
 ```
 prod:
   'prod*':
     - some_state
 ```
However it is possible to achieve this without multiple environments (by adding proper grains on minions):
 ```
 base:
   'role:prod':
     - match: grain
     - some_state
 ```
 The `role` grain on the minion has drawback. It is obvious by looking at such grain that it expresses membership. 
 Thus when such minion is compromised it is trivial to change its value to something that may reveal too much data to attacker.
 The first approach is free of this flaw, if attacker tinkers with `id` grain, the minion would have to be accepted on _Salt Master_
 - Group states by their purpose. Helps to organize the states
 
### Targeting
By default the shell-style globbing on minion `id` (_id_ is a grain data) is used, e.g.: `salt 'minion_id' test.ping` or
```
base:
  'minion_id':
    - some_state
```
[List of all targeting options](https://docs.saltstack.com/en/latest/topics/targeting/)

#### Targeting with grains
Grains are uploaded upon first contact and in general should not change, thus the grain targeting is safe.  
`salt -G 'your:grain:path:value' test.ping`, .e.g.: `salt -G 'os:Debian' test.ping`

#### Targeting with pillar
Pillar is actually cached not only on _Salt Minion_ but on _Salt Master_ too, in order to use pillar targeting, the
pillar data must be refreshed on master:  
 1. `salt '*' saltutil.pillar_refresh`  
 2. `salt -I 'some:pillar:value' test.ping`, or `salt -I 'some:pillar:value_prefix*' test.ping`

#### Compound targeting
Allows to mix all of the options using slightly different syntax:  
`salt -C 'G@os:Debian and I@redis:setup_type:cluster' test.ping`  
Find all of the available prefixes to be used [here](https://docs.saltstack.com/en/latest/topics/targeting/compound.html#targeting-compound)

## States
States can be defined using arbitrary syntax as long as proper [renderer](https://docs.saltstack.com/en/latest/ref/renderers/) is present. In order to specify different renderer, use shebang with renderer name.
```
#!py

def run():
  ...
```
Default renderer uses Jinja2+YAML (order matters). 

States that are defined like in [example](https://github.com/kiemlicz/util/wiki/Salt-configuration#states) wouldn't be of much use,
they are too static. States should use pillar and grain data to allow flexibility of configuration.

## Pillar
Based on everything the _Salt Master_ already knows about the minion and minion grain data the _Salt Master_ creates 
the pillar data and sends it over to minion.
Pillar is managed similarly to state files. It contains its own `top.sls` with data to minion matching and the actual pillar data

What to store in pillar data:
 - secrets
 - minion configuration
 - any data... this is the place where all of the variables and configs should be stored

It is even possible to include _Salt Master_ configuration files in the pillar data. 
In `/etc/salt/master.d/custom.conf` the setting: `pillar_opts: True` controls this.

### Environments aka pillarenv
Similarly to `saltenv`, `pillarenv` exists. The purpose is almost the same: to group pillar files within environments.

However... by default minion fetches pillar data from all matching environments, thus defeating the purpose of `pillarenv`.
Setting `pillarenv` in the minion configuration changes this behavior to select only this one defined environment.

### CLI
Inspect whole minion pillar data: `salt 'my_minion' pillar.items`  
Get pillar value: `salt 'my_minion' pillar.get my:nested:or_not_key`
