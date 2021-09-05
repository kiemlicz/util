Ambiguous term in salt documentation, overused to describe any piece of salt logic.  
The `*.sls` files contains state definitions, this is just the data file (YAML by default) the Salt translates into _State Module_ execution

# Core Modules 
## Execution Modules
[salt/modules](https://github.com/saltstack/salt/tree/develop/salt/modules)  
Custom: `salt://_modules`  

The `salt` or `salt-call` command executes exactly the _Execution Modules_  
Contrary to _State Modules_, _Execution Modules_ don't check any state, they just perform action.

`salt '*' cmd.run "ls /" cwd=/`  

`cmd` - the module name, the module name is either the `salt/modules/cmd.py` or `salt/modules/any_name.py` containing `__virtualname__ = "cmd"`  

`run` - the actual function definition, everything after function definition is the args and kwargs (for the actual function or for the salt state compiler)

`"ls /"` - first positional argument of [run function](https://docs.saltstack.com/en/latest/ref/states/all/salt.states.cmd.html#salt.states.cmd.run)

`cwd=/` - keyword argument

## State Modules
[salt/states](https://github.com/saltstack/salt/tree/develop/salt/states)  
Custom: `salt://_states`  

Enforces desired states on the remote. Under the hood they usually use _Execution Modules_

```
pkgs_pip:
  pip.installed:
    - name: pip_packages
    - pkgs:
      - google-auth
    - reload_modules: True
```

`pkgs_pip` - state ID

`pip` - _State Module_ name, maps directly to either `salt/states/pip.py` or `salt/states/any_name.py` containing `__virtualname__ = "pip"`

`installed` - the actual function name, naming convention: past tense.

`- name: pip_packages` the first positional argument, by convention called `name`. When the `name` is not passed the state ID is used as the `name`  

### Ordering states
Salt supports two ordering modes:
 1. _Definition order_: in the order of appearance in `top.sls` file, thus it is the filename that determines order. Then the states are executed 
 by the order of appearance in the state file itself. The `include`d files that were defined after **including** file are executed first. `inculde` takes precedence. 
 2. _Lexicographic order_: states are sorted by: their _name_, _function_ and then by _state ID_. Enable with configuration option: `state_auto_order: False`, the `include` statement in `sls` files
 doesn't affect the order at all.

Both options respect the [requisite statements](https://docs.saltstack.com/en/latest/ref/states/ordering.html#requisite-statements).  
The requisites take precedence over configured ordering.

[Full list of requisite statements and their usage](https://docs.saltstack.com/en/latest/ref/states/requisites.html).

If multiple states happen to be assigned same order number (the internal number that formally determines execution order),
then _Salt_ fallbacks to _Lexicographic ordering_.

### [Evaluating states](https://docs.saltstack.com/en/latest/ref/states/compiler_ordering.html) 
By default _sls_ files are written using in YAML format with Jinja templates. Both engines are not aware of each other.
Jinja templating starts before validating YAML.  

In other words:
 1. Jinja must produce valid YAML file
 2. YAML file must be a valid [highstate](https://docs.saltstack.com/en/latest/ref/states/highstate.html#states-highstate-example) data structure
 3. Highstate is compiled to lowstate (lowstate is a sorted list of state executions)
 4. _Salt_ executes the list in the order

The full evaluation and execution order:  
`Jinja -> YAML -> highstate -> lowstate -> execution`

It is very easy to misuse jinja. When the state starts to be unreadable, it is possible candidate to switch to different 
renderer (usually `#!py`).  
However user desired logic may be too complex still. Then writing custom _Execution Module_ or _State Module_ is a better idea.  

Additionally as the _State Tree_ grows, it is easy to fall into following trap (depicted by example):
```
clone_repo:
  git.latest:
    - name: https://github.com/kiemlicz/util
    - target: /tmp/util/
    - branch: master

{% for f in '/tmp/util/' | list_files %}
{% if f == '/tmp/util/README.md' %}

add_developer_{{ f }}:
  file.append:
  - name: {{ f }}
  - text: "added contributor: bla@o2.pl"
  - require:
    - git: clone_repo
    
{% endif %}
{% endfor %}
```
User assumed that the jinja will 'see' `clone_repo` changes. It is not true.  
Jinja is evaluated first, thus when this _sls_ file is applied first time, effectively the YAML looks like:
```
clone_repo:
  git.latest:
    - name: https://github.com/kiemlicz/util
    - target: /tmp/util/
    - branch: master
```
However during next run, the jinja will 'see' the changes (as they are already applied). Thus the output YAML will become:
```
clone_repo:
  git.latest:
    - name: https://github.com/kiemlicz/util
    - target: /tmp/util/
    - branch: master

add_developer_/tmp/util/README.md:
  file.append:
  - name: /tmp/util/README.md
  - text: "added contributor: bla@o2.pl"
  - require:
    - git: clone_repo
```
There are couple of options how to overcome such situation, most common involve:
 - writing custom _Execution Module_ or _State Module_
 - using [Slots](https://docs.saltstack.com/en/latest/topics/slots/index.html) (if you know what you are doing)

#### Slots
Relatively new _Salt_ feature, allows to store the result of _Execution Module_ and use it in next _Modules_ (during same run).  
Example:  
```
dnsutils:
  pkg.latest:
  - name: dnsutils

find_domain:        # works
  cmd.run:
  - name: "nslookup google.com"

the_state_id:       # fails
  test.show_notification:
  - name: some name
  - text: "the server ip: {{ salt['cmd.run']("nslookup google.com") }}"
```
Will fail because not-yet-existing command output is used as part of state definition.  
Using slots we can overcome this:
```
dnsutils:
  pkg.latest:
  - name: dnsutils

find_domain:        # works
  cmd.run:
  - name: "nslookup google.com"

the_state_id:       # works
  test.show_notification:
  - name: some name
  - text: __slot__:salt:cmd.run("nslookup google.com")
```

### Idempotence
It is tempting to wonder: is the state execution idempotent?

Is depends, e.g., the states like:
```
run_scripts:
    cmd.script:
        - name: do_dangerous_stuff.sh
```
are not guaranteed to be idempotent because everything depends on underlying: `do_dangerous_stuff.sh` script, so in general it is wise
to assume that such state is not idempotent.  
Moreover adding jinja constructs that modify underlying system also doesn't help (not advised though).

However _Salt_ provides requisite constructs that can be added to (not all) states: `onlyif` or `unless`

Thus it is possible to make _Salt_ states idempotent 

### Best practices
Check these two documents, they provide excellent details about how to create state properly:
 - [best practices](https://docs.saltstack.com/en/latest/topics/best_practices.html)
 - [formulas best practices](https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html)

# Data Modules
Contains runtime configuration, variables, secret data... data...

| Data\Authority | _Salt Master_ | _Salt Minion_ | Other |
|----------------|--------------|----------------|-------|
| Secrets | Pillar | SDB | SDB |
| Config | Pillar | Grains | SDB |

## Grains Modules
[salt/grains](https://github.com/saltstack/salt/tree/develop/salt/grains)  
Custom: `salt://_grains`  

Minion specific data, can be also specified in configuration file `grains: {}`, or set by master.  
Grains are refreshed on a very limited basis and are largely static data. If there is some minion specific data that
needs to be updated on the master then the _Salt Mine_ is the place to go.

## Pillar Modules
[salt/pillar](https://github.com/saltstack/salt/tree/develop/salt/pillar)  
Custom: `salt://_pillar`  

_Salt Master_ is authoritative over pillar data. Pushes pillar to minions that cache it. Minion may request pillar data
on its own. 

## SDB Modules
[salt/sdb](https://github.com/saltstack/salt/tree/develop/salt/sdb)  
Custom: `salt://_sdb`  

Used when neither _Salt Master_ nor _Salt Minion_ is authoritative over data. It could be used to pull secrets
from HashiCorp Vault or other keystores. If it is _Salt Minion_ that makes the call to _sdb_ it calls directly the third party
entity.
It is possible to use SDB modules in the _Salt Master/Minion_ config files:
```
client_id: sdb://module_name/secret_client_id
```
However it's impossible to bootstrap _Salt_ with custom SDB modules used in config already. 
During the _Salt Minion/Master_ startup the full config is read and parsed, thus any `sdb://<profile>/key` are evaluated
Use of custom SDB modules requires preceding: `sync_sdb`, which doesn't happen during initial bootstrap

# Event Modules and Reactor System
_Salt Master_ and _Salt Minion_ have their own event buses. Depending on the Module's function used to fire event, event may or may not be propagated
to other event buses (e.g. from Minion to Master and vice-versa).

Event always comprises of two things:
 1. event tag
 2. data dictionary
 
_Salt_ event system that uses _Event Modules_ is described in separate [section](https://github.com/kiemlicz/util/wiki/Salt-Events-and-Reactor) 

## Beacon Modules
[salt/beacons](https://github.com/saltstack/salt/tree/develop/salt/beacons)  
Custom: `salt://_beacons`  
Way to notify the master about anything. Works like a probe/sensor, e.g. disk is going full. 
Notifications use the _Salt Minion_'s event bus and are propagated to _Salt Master_.  
Internally beacons work in the following way:
 - minion's scheduler starts the beacon module's `beacon` function
 - the function fetches desired data in the most lightweight way possible
 - data is forwarded to _Salt Minion_ event bus
 
## Queue Modules
[salt/queues](https://github.com/saltstack/salt/tree/develop/salt/queues)  
Custom: n/a  
Helps to handle the events, sometimes it is desirable to enqueue incoming events and `pop` them sequentially instead of allowing asynchronous reactions to happen.

## Engine Modules
[salt/engines](https://github.com/saltstack/salt/tree/develop/salt/engines)  
Custom: `salt://_engines`  
Can be run on _Salt Master_ or _Salt Minion_, once started: runs forever in separate process. Commonly used to integrate
with external systems (like sending the notifications to slack) or fetching the external systems data under the _Salt_ infrastructure.

## Thorium Modules - experimental
[salt/thorium](https://github.com/saltstack/salt/tree/develop/salt/thorium)  
Custom: `salt://_thorium`  
Primarily created to add event aggregation, requires [additional configuration](https://github.com/kiemlicz/util/wiki/Salt-configuration#thorium).
Sometimes it is desirable to start a reaction once the set of `N` minions complete their `highstate` logic, not
every time each of the minions completes. This can be achieved with Thorium. 
Example of thorium state file that fires the event only when two `salt/custom/event` are received:
```
something:
  reg.list:
    - add: "some_field"
    - match: 'salt/custom/event'
  check.len_eq:
    - value: 2
send_when:
  runner.cmd:
  - func: event.send
  - arg:
    - thor/works
  - require:
      - check: something
```

# Result Modules
TODO
## Output Modules
## Result Modules

# Admin Modules
## Wheel Modules
[salt/wheel](https://github.com/saltstack/salt/tree/develop/salt/wheel)  
Custom: n/a  
Dealing with _Salt_ infrastructure itself, e.g., accept _Salt Minion_ key.

## Runner Modules
[salt/runners](https://github.com/saltstack/salt/tree/develop/salt/runners)  
Custom: `salt://_runners` (`runner_dirs` configuration option)  
Used exclusively by `salt-run` command. They are pure _Salt Master_ Modules, designed to run on master only.

## Cache Modules
[salt/cache](https://github.com/saltstack/salt/tree/develop/salt/cache)
Custom: `salt://_cache`

## Netapi Modules
[salt/netapi](https://github.com/saltstack/salt/tree/develop/salt/netapi)
Modules that expose Salt API, require configuration to enable

### Python client API
This is not the part of Salt's `netapi`, but a library for interaction with Salt  
Same that is used by Salt commands

# Integration Modules
TODO
# Utility Modules
TODO
