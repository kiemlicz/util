Salt accommodates multiple configurable transports (communication between master - minions):
 - TCP
 - ZeroMQ (default)
 - RAET (Rapid Asynchronous Event Transport)

## Architecture (ZeroMQ transport)
There is **no bi-directional** communication using one channel only
  
Master communicates with minions via _Pub/Sub bus_ - this is broadcast type. Internally named `Publisher`, uses TCP port 4505   
Thus **every** minion receives the master requests (the filtering happens on the minion).
Master computes the number of expected replies (if using wildcards or computation is impossible, master will always assume all cached minions could reply).  
Minions sends their requests and replies via _Direct bus_, this channel is private for master-minion pair. Internally named `ReqServer`, uses TCP port 4506 

For example, all of the following calls are insecure:  
`salt '*' grains.set some:password 'afm4o'`,  
`salt 'minion' grains.set some:password 'afm4o'`,  
`salt 'minion' state.apply db.setup pillar='{"some": {"password": "afm4o"}}'`  

On the other hand:
`salt 'minionX' saltutil.refresh_pillar` is secure.  
Minion (and possibly all other minions) will receive the request to
refresh the pillar data. However only `minionX` will establish private secure channel with master, which will use to fetch it's own private pillar data.

## Detailed job flow
 1. User issues command on the CLI, `salt 'minion' test.ping`
 2. `salt` uses `LocalClient` class for connection with _Salt Master_'s `ReqServer` on TCP port 4506
 3. Job is issued over established connection
 4. `ReqServer` passes the job to worker processes (`MWorker`) on the _Salt Master_
 5. Worker validates the job (e.g. is user allowed to perform it)
 6. Worker send the publish command to all minions. Publish command represents the job to be executed. 
 Worker does this by sending an event on _Salt Master_ event bus. In the form of: `salt/job/jid/new`, where `jid` is a generated job ID.
 7. From _Salt Master_ event bus, event is encrypted and transferred to actual `Publisher` that sends the message to
 **all** connected minions
 8. Minions already have session established with _Salt Master's_ `Publisher` (port 4505), where they await commands.
 9. Minions decrypt the message
 10. Minions check if the message is targeted for them
 11. Job is executed
 12. The result of the job execution is encrypted and send back to master to `ReqServer` TCP port 4506.
 13. `ReqServer` forwards the result to `MWorker's`
 14. `MWorker` decrypts the received result, forwards it to _Salt Master_ event bus.
 15. One of the _Salt Master_ event bus listeners is a `LocalClient` that has been waiting for this result
 16. `LocalClient` stores the result, waits until all expected minions reply (or timeout occurs)
 17. Result is displayed back to CLI
 