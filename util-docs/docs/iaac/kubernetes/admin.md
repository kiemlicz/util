# Kubernetes components
Kubernetes Cluster spans over multiple nodes, the _master_ (Control Plane) should be separated from _worker_ Nodes

![components](https://d33wubrfki0l68.cloudfront.net/7016517375d10c702489167e704dcb99e570df85/7bb53/images/docs/components-of-kubernetes.png)

## kube-apiserver
Master only component. Accepts user request. Stores resources definitions in `etcd`.

## etcd
Master only component. Key-value store that is highly available. Used to store all cluster data.

## kube-scheduler
Master only component. Materializes user requests, `watch`es the kube-apiserver, decides where and when schedule PODs.
PODs definition may contain some data that affects `kube-scheduler`:
 - `affinity/anti-affinity`
 - `nodeSelector`
 - `taints/tolerations`
 - `reservations/limits`
 
It is possible to write custom scheduler 

## kube-controller-manager
Master only component. Controllers execute routine tasks to synchronize desired state (typically called `spec`) with observed state.
Notable mentions:
 - Node Controller - monitors Node lifecycle, responds when the Node goes down
 - [Replication Controller](Kubernetes-Controllers.md) - manages `*-controller`s, e.g., `deployment-controller`
 - Endpoints Controller - populates Endpoint
 - Service Account Controller - creates accounts and access tokens for namespaces

[Full list of controllers](https://github.com/kubernetes/kubernetes/tree/master/pkg/controller)
 
## kubelet
Master/Worker component. Resides on every Node. Connects to the `kube-apiserver`. Starts the actual containers via the container runtime. 
Provides health-checks

## kube-proxy
Master/Worker component. Main network component, watches the `service`s and materializes their rule on the Nodes (e.g. handles `iptables`)

# References
1. https://kubernetes.io/docs/concepts/overview/components/
2. https://engineering.bitnami.com/articles/a-deep-dive-into-kubernetes-controllers.html
