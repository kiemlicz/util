Essentialy - a directory that will be accessible by POD, preserving state independently of POD lifecycle.  
Example (simplest) usage of volume
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
      volumeMounts:
      - mountPath: /var/tmp
        name: vartmp
  volumes:
  - name: vartmp
    hostPath:
      path: /mnt/testing 
```
There are [numerous volume types](https://kubernetes.io/docs/concepts/storage/volumes/) that can be used, `hostPath` is actually the most test-purpose only.  
It is possible to mount `ConfigMap` as a volume.  

Typically you have `PersistentVolume` (PV) _resource_ (or have some Cloud provider prepare that for you) and you just mount it to the PODs.
The `persistentVolumeClaim` (PVC) is used to represent the request for the storage (PV).

There are two main types of Persistent Volumes provisioning:
1. Static  
It is the administrator that prepares volumes. Use `selector` in PVC, without providing `storageClassName` to use static provisioning

2. Dynamic  
Based on `StorageClass` the `PersistentVolume` will be automatically created for given PVC. Use `storageClassName`.

Example POD with `PersistentVolume` Statically provisioned (`StorageClass` is not used at all)
```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
  labels:
    name: example-pv
spec:
  capacity:
    storage: 1Mi  
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  ##storageClassName: local-storage
  #hostPath:
  #  path: /mnt/testing
  local:
    path: /mnt/testing
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - k8s1
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
spec:
  ##storageClassName: local-storage
  selector:
    matchLabels:
        name: example-pv
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Mi
--- 
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
      volumeMounts:
      - mountPath: /var/tmp
        name: vartmp
  volumes:
  - name: vartmp
    persistentVolumeClaim:
      claimName: example-pvc
```

The `persistentVolumeReclaimPolicy` tells what happens to `PersistentVolume` after released from claim. Defaults:  

`Retain` for statically provisioned `PersistentVolume`  

`Delete` for dynamically provisioned `PersistentVolume`

The `PersistentVolume` must support different (than default) policy setting.
