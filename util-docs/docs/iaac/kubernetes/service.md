Services create rules for accessing Pods  
Services route traffic to the ready Pods only  
Services matches Pods using selectors  
Services expose DNS name that is available across the cluster.  
The full service name: `name.namespace.svc.cluster.local`  
Default resolution policy in Kubernetes is `ClusterFirst`:
 - DNS query is routed to `dnsmasq` (running in `kube-dns` pod)
 - `dnsmasq` routes the request to:
    - `kube-dns` if the name ends with a cluster suffix 
    - to the upstream DNS server otherwise

# Basics
Name resolution is configured in `/etc/resolv.conf`.  
By default pods contain `resolv.conf` with roughly:
```
nameserver 10.10.10.10
search namespace.svc.cluster.local svc.cluster.local cluster.local something.cloud.provider.specific
options ndots:5
```
If the requested DNS name contains fewer than 5 dots then the search domains are checked. 
If there is no match then the name is treated as an absolute name  
The FQDN domains (the ones ending with `.`) are always treated as absolute.
Thus if the pod needs to resolve the name that is known to be external to the cluster: it is good to configure that name as FQDN in the application.
The pod will make fewer (number of `search` option entries) DNS queries  
It is also possible to customize `resolv.conf` using `dnsConfig` pod's section

# Headless
```
type: ClusterIP
clusterIP: None
```
No IP is allocated. DNS is configured:
- if selectors are used then DNS returns all matching Pods
- if selectors are not configured then:
   - DNS returns `CNAME` records for ExternalName -type Services
   - DNS returns records for and Endpoints that share a name with this Service, for all other types

Using headless service it is possible to expose pods hostname for cluster availability (required: `hostname` and `subdomain` on the pod)
   
# ClusterIP
`type: ClusterIP`

Default Service type, guarantees unique IP across the cluster. This IP 'lives' only in iptables and is maintained by `kube-proxy`.  
By default uses round-robin to pick pods.

# NodePort
`type: NodePort`

Gives access from outside of the cluster. Opens socket with high port on every node thus allowing to access the service 
from outside of the cluster using node IP (with that high port)

# LoadBalancer
`type: LoadBalancer`

Gives access from outside of the cluster. This is cloud-specific. Creates the load-balancer-type resource in cloud provider
