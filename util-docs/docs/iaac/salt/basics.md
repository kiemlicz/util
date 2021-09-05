Salt is primarily a configuration management solution and remote execution engine.  
Thanks to the latter, many use-cases can (but not necessarily should) be covered using just this one tool.

# Basics
| Term | Meaning |
|------|---------|
| minion | slave, managed host |
| sls | _salt state file_, file that represents the state the system should end up in |
| pillar | sensitive data, tree like structure, targeted and securely send to matched minions |
| grain | minion data, static information, rarely refreshed on master, contain minion specific data only (like OS name) |

[Full glossary](https://docs.saltstack.com/en/latest/glossary.html)

# Architecture
Event-based, highly [modular](https://docs.saltstack.com/en/latest/ref/index.html) and highly [customizable](https://docs.saltstack.com/en/latest/ref/modules/).
It is fairly easy to add your own state modules as well as alter existing ones.       
Runs: 
* master-slave (separate master node that provisions minion nodes)
* master-less (the node provisions itself)

Supports both management modes:
* push (the master sends the config updates to minions)
* pull (the minions check with master for config updates)

Can operate:
* with agents (application installed on minion)
* [agent-less](https://docs.saltstack.com/en/latest/topics/ssh/) (no application installed on minion)

_Salt State Files_ express the desired... state on the provisioned minion.  
States are matched to minions using (primarily) [`top.sls` file](https://docs.saltstack.com/en/latest/ref/states/top.html).  
Each _state_ is then executed on targeted minion (slave). By default minions are targeted using minion _id_ - special generated grain (its default value is the minion hostname).  
Detailed description how does the state execute on minion is provided in [Modules](https://github.com/kiemlicz/util/wiki/Salt-Modules) section 

Information about how to interact with _Salt_ can be found in [usage](https://github.com/kiemlicz/util/wiki/Salt#usage) and in [scripts](https://github.com/kiemlicz/util/wiki/Salt-Scripts) sections 

## Details
Salt architecture consists of [multiple components](https://docs.saltstack.com/en/latest/topics/development/modular_systems.html),
it is best to describe them using layered approach:
 - [minion](https://github.com/kiemlicz/util/wiki/Salt-Minion)
 - [master](https://github.com/kiemlicz/util/wiki/Salt-Master)
 - [transport](https://github.com/kiemlicz/util/wiki/Salt-Transport)
 - [scripts](https://github.com/kiemlicz/util/wiki/Salt-Scripts)
 - [modules](https://github.com/kiemlicz/util/wiki/Salt-Modules) 
 
# Usage
This section contains only brief description of how to interact with Salt using CLI.  
For more complete overview refer to [scripts](https://github.com/kiemlicz/util/wiki/Salt-Scripts).

_Execution Module_ execution (dissection of the `salt` command):

`salt '*' execution_module_name.function_name [arguments_list] [kwargs]`  
 - `salt` is the python script that accepts user commands and passes them to _Salt Master_ process.  
 - `'*'` selects minions which will execute user function. By default the shell-style globbing is used on minion id.  
 - Find [`execution_module_name` in docs](https://docs.saltstack.com/en/latest/ref/modules/all/index.html) or within [Salt sources](https://github.com/saltstack/salt/tree/develop/salt/modules).  

Example: `salt '*' test.ping`

State execution (or rather state application):  
Check what states are going to be applied: `salt '*' state.show_top`  
Execute all matching states from given environment: `salt '*' state.highstate [saltenv=base]`  
Execute single state: `salt '*' state.apply <statename> [saltenv=<env>]`

# References
1. https://repo.saltstack.com/
2. https://docs.saltstack.com/en/getstarted/config/functions.html
3. https://docs.saltstack.com/en/latest/topics/tutorials/states_pt1.html
4. https://docs.saltstack.com/en/latest/ref/states/highstate.html
5. [Great presentation](https://vimeo.com/289106306/7fd5601ce6) from [@carsonoid](https://github.com/carsonoid)
6. https://docs.saltstack.com/en/latest/ref/configuration/master.html
