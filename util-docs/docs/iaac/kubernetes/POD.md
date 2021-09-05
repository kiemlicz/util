Main execution unit of Kubernetes cluster
  
`kubectl get pods -o wide` will inform about status, number of restarts, POD readiness or assigned node.  

# Status
The status roughly traverses:
Pending -> Running -> Succeeded/Failed -> Completed -> CrashLoopBackOff (if policy says so)

The POD default `restartPolicy` is `Always`, which means that if POD gets to Completed state, it will restart automatically.

To specify container command and/or args: `command`, `args`. 
If the Docker runtime is used then the `command` will override `ENTRYPOINT` and `args` will override `CMD`

Minimalistic POD yaml example:
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: pod
  name: example
spec:
#  restartPolicy: OnFailure
  containers:
    - image: httpd
      name: example
 #     command:
 #      - "echo"
 #      - "A"
```

# Probe
Such POD once reaches the Running state, is immediately marked as Ready (`kubectl get pod example`).
This is due to the fact that example POD didn't provide `readinessProbe` - the mechanism which informs the Kubernetes that
the POD is ready to accept the traffic.  
Example enriched with `readinessProbe`
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: pod
  name: example
spec:
  containers:
    - image: httpd
      name: example
      readinessProbe:
        exec:
            command:
              - cat
              - /tmp/healthy
        initialDelaySeconds: 5
        periodSeconds: 5
```

There are two types of probes:
1. `livenessProbe` - inform that the POD needs to be restarted
2. `readinessProbe` - inform that the POD won't accept traffic

Both of them use three different types of materializing checks: 
1. `exec` execute arbitrary command
2. `httpGET` perform HTTP GET request and succeed if 2XX code received
3. `tcpSocket` open TCP socket and try to establish a connection (three-way handshake only)

Both probes accept different thresholds, periods and inital delays.  
Using `port-forward` for accessing non-ready PODs bypasses the non-routing restriction.

# Resources
POD resources may be limited to not use all of node available resources.
Adjusted using `requests` and `limits`
```
apiVersion: v1
kind: Pod
metadata:
  name: example
spec:
  containers:
  - image: httpd
    name: example
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 1000m
        memory: 256Mi
```
<tools container awareness e.g. ps vs free>
<oomkiller container awareness>

## `requests`
Kubernetes Scheduler uses this value to place the POD on _the best_ node.
This is the value that the node will at least reserve for POD

## `limits`
<TODO>

# Init containers
Run certain scripts/procedures during POD startup. 
Affects the POD status change path:  
Pending -> Init -> PodInitializing -> Running -> Succeeded/Failed -> Completed -> CrashLoopBackOff (if policy says so)  
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: pod
  name: example1
spec:
  containers:
    - image: httpd
      name: example1
  initContainers:
    - image: debian:stretch-slim
      name: ini
      command:
        - "sh"
        - "-c"
        - "sleep 5"
```
Debug with `kubectl logs example1 -c ini`

# Termination
POD may be terminated not only upon user request but also:  
 - the scheduler may decide to move the POD to other node
 - some auto-scaling mechanisms
 - upgrades

Termination:  
1. for all containers in POD: `SIGTERM` sent to the PID 1
2. `terminationGracePeriodSeconds` countdown starts
3. if the timeout occurs and container(s) is still alive the `SIGKILL` is send

# Tricks

Throw-away debug container:  
`kubectl run -it --rm name --image=the_image --restart=Never -- sh `

busybox: `kubectl run -it --rm busybox --image=busybox --restart=Never -- sh`    
debian: `kubectl run -it --rm debian --image=debian --restart=Never -- bash`
