Agent daemon that runs on the remote (managed) node.    
Receives commands from the _Salt Master_ and responds with the results, can operate autonomously as well.
  
Runs directly on top of the OS (Windows, Linux, Mac), requires python (2.7 or 3.5).

Identified by ID which is equal to hostname by default. Override in settings:
```
id: desired_id
```
If during the minion lifetime the hostname changes and there is no `id` setting in the config the minion ID is not updated 

## Operation
 1. upon **first** minion start the ID is generated using following [procedure](https://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html#minion-id-generation)
 2. minion generates keypair
 3. sends public key to the _Salt Master_
 4. waits for _Salt Master_ to accept the key (there are multiple ways to accept the key, e.g., [salt-key](https://github.com/kiemlicz/util/wiki/Salt-Scripts#salt-key))
 5. _Salt Master_ generates symmetric key, encrypts it with _Salt Minion_ public key and sends back
 6. _Salt Minion_ has established secure connection
 7. _Salt Minion_ sends grains via secure channel

_Salt Minion_ is ready to accept master requests, all further state file rendering happens on minion
