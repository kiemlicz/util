Typically PODs are scheduled via higher-level abstraction that relies on `controller`s.  
Controllers 'find' PODs using `.spec.selector` 

# Deployment
Common method to create the groups of PODs with regards to number of instances running. "Replaces" `ReplicaSet`  

1. No POD location guarantees by default 
2. PODs will be suffixed with random string
3. PODs **started** at the same time 
4. PODs are updated one after another ("previous" one must be `READY` in order to continue) by default. 
   Refer to [`DeploymentStrategy`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#deploymentstrategy-v1-apps)) for all options
   - `Recreate` - Terminate all, start all
   - `RollingUpdate`-  Don't let all PODs go down, upgrades gradually

# StatefulSet
Don't use if 3. is not required

1. No POD location guarantees by default
2. By default started one by one (previous one must be `READY` in order to continue). It is possible to start all at once (see `podManagementPolicy`). Order of deletion is not specified.
3. PODs have stable network identifier (predictable, ordered names instead of random hash). This includes PVC as well, the Nth POD will use Nth PVC.
   The headless `Service` is required (must be added manually)
4. Updated in order (hi -> low), regardless of `podManagementPolicy` setting by default.
   Refer to [`StatefulSetUpdateStrategy`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#statefulsetupdatestrategy-v1-apps)
   - `OnDelete` - no automatic action when update is triggered
   - `RollingUpdate` - Don't let all PODs go down, upgrades gradually. `StatefulSet` includes [`partition`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#rollingupdatestatefulsetstrategy-v1-apps)
     parameter (default = 0). Only PODs with ID greater than or equal `partition` will be updated, the rest will not, even when manually deleted.

Mind:
https://github.com/kubernetes/kubernetes/issues/82612 (change cause message doesn't work for `StatefulSet`)  
https://github.com/kubernetes/kubernetes/issues/67250 (cannot `rollout undo statefulset` from broken `StatefulSet` replica)  
https://github.com/kubernetes/website/issues/17842 (headless `Service` requirement clarification)

# DaemonSet
The only allowed POD `RestartPolicy` is `always` 

1. POD location guarantees: one POD on each node
2. PODs **started** at the same time
3. Adding `Nodes` adds `DaemonSet`s PODs (with regards to `tolerations`, `nodeSelector`, etc. - see [this doc](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#taints-and-tolerations))
4. PODs are updated one after another ("previous" one must be `READY` in order to continue) by default.
   Refer to [`DaemonSetUpdateStrategy`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#daemonsetupdatestrategy-v1-apps)
   - `RollingUpdate` - Don't let all PODs go down, upgrades gradually.
   - `OnDelete` - no automatic action when update is triggered
     
# ReplicaSet
In general: replaced by `kind: Deployment`. Can 'capture' other manually created PODs if they match labels.
Internally, the `Deployment` uses `ReplicaSet`

1. No POD location guarantees by default
2. Doesn't support updates
3. Doesn't support `rollout` commands
4. Starts and terminates all at once

## ReplicationController
The ReplicationController simply ensures that the desired number of pods matches its label selector and are operational.
Was replaced by `ReplicaSet`

# Job
Schedules PODs and ensures that specified number of them **completes** successfully.
It is possible to run PODs in parallel.
The `Job` may be used for [work queue processing](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/),
just remember to set `.spec.completions` to 1 and `.spec.parallelism` > 0 

1. No POD location guarantees by default
2. Doesn't support `rollout` commands
3. By default runs only one POD

# Usage
For interaction with selected controller kind the `kubectl rollout` command is used.  
The `.spec.template` must be changed in order to trigger update, otherwise the same deployment `revision` is used

| Information | Command |
|-|-| 
|Status | `kubectl rollout status <kind, e.g.: deployment, statefulset> <name>` |  
|History (The `CHANGE-CAUSE` is copied from annotation `kubernetes.io/change-cause`), more details can be obtained using `--revision`|`kubectl rollout history <kind e.g. deployment> <name> [--revision=N]`|
|Rollback|`kubectl rollout undo <kind e.g. deployment> <name>`|
