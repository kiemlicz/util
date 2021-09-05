Kubernetes is the **container** orchestration tool.  
Its primary job it to ensure that given container is running with regards to given constraints (e.g container X requires N mb of memory or container X must be replicated N times on different physical nodes).

Kubernetes covers more use-cases: it is a platform for automatic deployment, scaling, HA and orchestration of containerized applications

## Terminology
Kubernetes introduces multiple concepts.

The main one is: _the resource_ (aka. object)

In order to list all of the Kubernetes resources use: `kubectl api-resources`

### Kubernetes Resources
The handy command: `kubectl explain <resource>`, for nested fields: `kubectl explain <resource>.<field>`

#### Node 
Worker machine, runs _Services_, capable of running _Pods_. Either VM or physical machine

#### Pod 
Resource
  
The 'execution' unit of Kubernetes.
Representation of one or more application containers (Docker or [rkt](https://github.com/rkt/rkt)) or shared resources for those containers.
Shared resources are available for all containers in the POD.
All containers within the POD share the same IP address and can communicate via loopback interface 
PODs are ephemeral.

#### Namespace 
Virtual cluster, scope for names. 
In order to find out if given _resource_ is affected by namespace use: `kubectl api-resources --namespaced=true`,
all of the listed resources respect the namespace setting. 

#### Deployment
Configuration how to create/update instances of the application

#### Service 
Set of _Pods_ with policy how to access them (e.g. load balancing or service discovery for _pods_)

#### Controller 
_Pods_ manager (handles, e.g., pod replication). Given information about desired number of PODs ensures the desired number of them is running.

#### Volume
Local storage on the POD is ephemeral. When the POD is destroyed, the POD data is gone forever. In order to enable 'persistent' storage - use volumes.

### Non-resource concepts

### Labels
Key-value pairs. Used to group together set of objects. Each object can have multiple labels, 'same' label can be attached
to multiple objects

## Basics
The PODs are the execution units submitted by the 'user', however creating, submitting PODs one by one would be tedious.  
This is solved by using e.g., deployment, statefulsets or daemonsets. They provide policies for scheduling multiple PODs.

Containers within one _POD_ share IP address. Tightly coupled containers should run within one Pod.
Pod provides two kinds of shared (by pod's containers) resources: _networking_ and _storage_.

Services match a set of pods using labels and selectors. Services are published or discovered either via DNS or environmental variables.

Services by default are visible within the cluster only and there is no way to access them from the outside of the Kubernetes cluster.

In Kubernetes following networking rules hold true:
 1. All containers/pods can communicate with all other containers/pods without NAT
 2. All Nodes can communicate with all containers/pods (and vice-versa) without NAT
 3. The IP that a container sees itself as is the same IP that others see it as

`Kubectl` is used to interact with the cluster.    
If you have multiple clusters, list them with: `kubectl config get-contexts`, 
switch between them with: `kubectl config use-context CONTEXT_NAME`  
`kubectl` commands supports both: imperative and declarative management:  
 - `kubectl create -f your.yaml` - imperative  
 - `kubectl apply -f your.yaml` - declarative

In order to get detailed information about any part of your deployment use `kubectl describe <kind>`.  
The term `kind` is defined in this [manual](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/) (it can simply be a `pod`, `service` or `deployment`)
In order to debug what actually happens within Kubernetes cluster: `kubectl get events --sort-by='{.lastTimestamp}'` 

## Setup
Setup depends on the number of nodes used for cluster

### Single-node
Use [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/).  
It uses either KVM or VirtualBox as docker host.  
In order to increase default limits of the VM, it must be destroyed first: `minikube delete; minikube start --memory 12288`

### Multi-node
TODO

# References
1. https://kubernetes.io/docs/user-journeys/users/application-developer/foundational/
2. https://coreos.com/rkt/docs/latest/rkt-vs-other-projects.html
3. https://vimeo.com/245778144/4d1d597c5e
4. https://www.magalix.com/blog/kubernetes-cluster-networking-101
5. https://pracucci.com/graceful-shutdown-of-kubernetes-pods.html