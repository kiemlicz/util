# [Reactor System](https://docs.saltstack.com/en/latest/topics/reactor/index.html)
**Not** a Module, [configured separately](https://github.com/kiemlicz/util/wiki/Salt-configuration#reactor), native part
of _Salt_, used to react to different events.  
Reactor is the go-to place to create 'self-healing' or 'fully-automated' solutions. Reactions are matched on the _Salt Master_.  
The reaction `sls` files follow the same rules of compiling (they have default Jinja+YAML renderer), however they are limited in
terms of available _Dunder Dictionaries_.  
Additional: `data` dictionary is available for reactions which contains event data.

## Reaction types
The `sls` reaction files must contain reaction type in front of `execution_module_name.function_name`

### Local reaction
Runs _Execution Module_ on targeted minions (not necessarily a "local"). Example:
```
highstate:
  local.state.highstate:
    - tgt: {{ data['id'] }}
```
This example runs [highstate](https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.state.html#salt.modules.state.highstate) on `data['id']` minion

### Runner reaction
Runs [_Runner Modules_](https://docs.saltstack.com/en/latest/ref/runners/all/index.html) on the _Salt Master_. Centralized _Salt Masters_ view
allows to create complex flows easily. Most widely used _Runner Module_ for this purpose is the _Orchestrate Runner_. 
```
redis_cluster_orchestrate:
  runner.state.orchestrate:
    - args:
      - mods:
        - redis.server._orchestrate
      - saltenv: server
```

#### [Orchestrate Runner](https://docs.saltstack.com/en/latest/topics/orchestrate/orchestrate_runner.html#orchestrate-runner)
In _Salt_ terminology, the _highstate_ is a collection of states applied to one minion.  
Collection of states applied to multiple minions with inter-minion dependencies could be called _Orchestration_.  
_Orchestrate_ is more generic term than _highstate_.  
As this is _Runner Module_ it can be directly called from CLI: `salt-run state.orchestrate kubernetes._orchestrate.cluster saltenv=server`  
Combined with _Salt_ event system allows to create multi minion-aware reactions.

`state.orchestrate` Module accepts `mods` argument, this is the `sls` file list with actual orchestration logic. Example of `redis.server._orchestrate`: 
```
refresh_pillar:
    salt.function:
    - name: saltutil.pillar_refresh_synchronous    # saltutil.pillar_refresh_synchronous doesn't exist, see below for explanation 
    - tgt: {{ salt['pillar.get']("redis:coordinator") }}

cluster_met:
    salt.state:
    - tgt: {{ salt['pillar.get']("redis:coordinator") }}
    - sls:
      - "redis.server._orchestrate.met"
    - queue: True
    - require:
      - salt: refresh_pillar

# some more logic
# ...
```
_Orchestrate Runner_ accepts other `sls'es` evaluates them on _Salt Master_ and invokes them on desired targets. 
These `sls'es` contain regular salt [states/functions or even _Runner Modules_](https://docs.saltstack.com/en/latest/topics/orchestrate/orchestrate_runner.html#examples).  
To simplify:
 1. Some situation triggers event
 2. Event is propagated to _Salt Master_
 3. _Salt Master_ checks if it can find reaction
 4. Reaction is rendered if found.
 5. Reaction executes _Runner Orchestrate Module_ if `runner.state.orchestrate`
 6. _Runner Orchestrate Module_ renders `mods` on the _Salt Master_
 7. _Runner Orchestrate Module_ executes functions on desired targets.

The most typical orchestrate `sls` files will comprise mostly of [`salt.[function|state]`](https://docs.saltstack.com/en/latest/ref/states/all/salt.states.saltmod.html) calls as they
accept the `tgt` parameter and thus can delegate the call to minions.

Aforementioned example contains unfortunate 'gotcha' in Salt.  
Typically _Salt Master_ may want _Minions_ to refresh the Pillar data prior to invoking desired states.
Thus calling `saltutil.pillar_refresh` prior to the states execution seems like viable solution.  
However it may (and usually will) not work, because `pillar_refresh` function actually doesn't refresh the Pillar on _Salt Minion_.
This particular function is asynchronous by default - which is inconsistent with most of the states that are synchronous.

### Wheel reaction
Runs [_Wheel Modules_](https://docs.saltstack.com/en/latest/ref/wheel/all/index.html#all-salt-wheel) on the _Salt Master_

### Caller reaction
Used for Masterless Minions. The minion must be properly [configured](https://docs.saltstack.com/en/latest/ref/engines/all/salt.engines.reactor.html#module-salt.engines.reactor).
Runs _Execution Modules_ on the minion

## Reactor state files limitations
Matching and redering reaction `sls` files is done sequentially in single process. Because of this, the reaction `sls` files should contain
very few reactions. Also heavy jinja logic within reaction `sls` files can choke whole _Reactor System_.  
Reactor doesn't support `require` or other requisite statements.  
Pillar and grain data are not available.  
Thus any time, some complex logic is required to handle event the `state.orchestrate` should be used as a reaction.  

[Example of typical flow (logic moved to orchestrator)](https://docs.saltstack.com/en/latest/topics/reactor/index.html#advanced-state-system-capabilities)
