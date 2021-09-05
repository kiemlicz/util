Originally LXC-based, widespread. Created for shipping and running applications. Encourages running **one process per container**.

## Basics
| term | meaning |
|-|-|
| image | Packaged application along with environment. Product of `docker build` command. Snapshot of a container. Analogous to the concept from _Object Oriented Programming_: `class` |
| container | Running instance of image. Analogous to the concept from _Object Oriented Programming_: `class` instance |
| tag | Extra information appended to image name. Helpful for enclosing image version information, if omitted: `latest` is assumed |
| registry | Repository that stores Docker Images, can be public or private |
| Dockerfile | Text file, contains [commands](https://docs.docker.com/engine/reference/builder/) that assemble image |

Each image is identified by ID, can contain different names and tags.  
Image name contains of slash delimited name components, with optionally repository name prefixed. If the name doesn't contain 
registry name, then the public `docker.io` is assumed.

The process specified as `ENTRYPOINT` in Dockerfile becomes PID 1 process, it means that it will not handle SIGKILL signal.

The container lifetime is equal to the encapsulating (`ENTRYPOINT`s) process lifetime. The process dies, the container dies too.

## Usage
Common commands:

| operation | command |
|-|-|
| Build image from `Dockerfile`. Invoke passing directory containing `Dockerfile` or pass the dockerfile with `-f`. The mandatory argument is called _build context_ - all dockerfile instructions are relative to that path and all non-ignored files from that directory are send to Docker engine | `docker build -t my-tag .` [Read more](#Building-images) |  
| Create and start container (simplest form) | `docker run --name <some_name> <image tag or name> [args]` |
| Stop container | `docker stop <container name or id>` |
| Remove container | `docker rm <container name or id>` |
| Remove image | `docker rmi <image name or id>` |
| Push image to registry | <ol><li>Tag image with repository URL first. Mind that repo may support the `v1` and/or `v2` 'naming' format. Briefly speaking: `v1` format doesn't support multiple path segments in image name, thus image: `rootName/subName` is invalid. For `v2` it is fine: `docker tag <image> <repourl>/<name>:<tag>`</li><li>Login to desired repository, `docker.io` is the default `docker login <repourl>` <li> `docker push <repourl>/<name>:<tag>` </li> </ol> |
| Show running containers | `docker ps` |
| Show container/image details | `docker inspect container_or_image_name` |

### Building images
[`Dockerfile`](https://docs.docker.com/engine/reference/builder/) contains all of the needed instructions to build the image with given application.  
Each instruction corresponds to filesystem layer. 
Image is built within _build context_ (the directory passed to `docker build` command - simply speaking).
All `COPY`-kind instructions are relative to that _build context_.  
The bigger the _build context_ (directory contents and size) the longer it takes to send them to Docker engine. 

#### Design goals when building images
There is a lot of things to keep in mind when building images. 
Many of them will be containerized-application specific: different set of guidelies for JVM application, python application, etc.

However there are some fundamental, containerized-application agnostic set of rules:

##### image size
The image is never downloaded once and there is a difference when downloading over 1GB image vs 100MB. 

Storage is also limited especially when images doesn't re-use the layers.

Huge images impact the downtime of your application, the bigger the image, the longer it takes to download it, the longer the downtime.
When the Kubernetes reschedules the POD to another Node which doesn't contain the image (or the image has changed), the time user waits for application is also longer 

Security the fewer the libraries in container the better,

The main goal when building the image should be: 
 - minimize the number of layers, the new layer is created only with: `COPY`, `RUN` and `ADD` commands.
 - use cache as much as possible. When the `Dockerfile` processed, each instruction is examined if its outcome is present in the cache already. 
 The `ADD` and `COPY` will check if the underlying file has changed, the `RUN` commands will check only if the command string has not changed.
 Thus building the image with `RUN apt-get update` second time won't update the latest packages.
 - once the cache is invalidated (instruction that misses cache occurred), all subsequent instructions won't check the cache

The verify layer re-use: `docker system df -v`

##### one application in container
 - management of the image that ships one application is easier: one log source, one application to monitor. Usage is easier too, 
 as there is no need for `supervisord`-like tools that govern multiple applications inside one container.
 - decoupled dependencies, easier to re-deploy

##### process reaping
When the (main) application spawns processes inside of container it's the application's responsibility to cleanup process after it completes.
Usually it was done by `PID 1 init` process, but the docker lacks one (by default at least)  
Since container uses its own `pid` namespace, as long as the container lives, the host's `init` process cannot clean orphaned processes.
 
#### Image types
There are two types of images in docker terminology:
 - _parent image_ - the image that is specified in `FROM` clause. Your image is based on _parent image_. Your image after build becomes parent image.  
 - _base image_ - the image that has no `FROM` or `FROM scratch`

Most `Dockerfile`s use _parent images_ in their `FROM` clause.

##### [Building base images](https://docs.docker.com/develop/develop-images/baseimages/)
In order to build base image:
 - use debootstrap for Debian-based distributions (tool that installs Debian-based distributions into given filesystem) 
 - archive it and `docker import image.tar name` 

It is also possible to build base image from `Dockerfile`:  
```
FROM scratch
ADD some_binary /
CMD ["/some_binary"]
```
Such image will be able to execute the specified binary only.
 
### Debugging
Failed container can be pretty easily debugged
1. Grab exited container ID  
`docker ps -a`
2. Create image  
`docker commit <container id>`
3. Run image corresponding to failed container, overriding its potential `ENTRYPOINT`  
`docker run -it --entrypoint /bin/bash <image id>`

Live container can be debugged as well:
1. Grab the container name or ID: `docker ps`
2. Attach to the container with: `docker exec -it <container id> /bin/bash`

## Networking
Networking system in Docker is configurable. It is possible to set different networking driver for containers using:
`docker run --network=host ...`

### bridge
Default driver, creates the bridge that connects all containers withing Docker host. Docker host manages IP addresses and `iptables` rules
governing inbound/outbound traffic. From Docker host it should be possible to reach any port on the running container (host has routing configured for containers subnet: `ip r s`)
However by default containers will be unreachable from outside (outside of Docker host). In order to tell Docker host, 
that it should add `iptables` rules allows access to containers the port publish option must be used: `docker run... -p 8080:80 ...`.  
The `-p hostPort:containerPort` maps (TCP by default) port 8080 on the host to the container port 80.   

### host 
Uses the host networking interfaces. No network isolation. The `ip a` output from within the container will print same
entries as `ip a` on the Docker host

### overlay
Use when multiple containers need to communicate with each other and containers are scattered among different Docker hosts

### macvlan
TODO

### none
Disables networking

### custom
TODO

## Volumes
TODO

## Configuration
`dockerd` uses following configuration files:

`/etc/docker/daemon.json`

`/etc/default/docker` (for Debian based OSes)

### Change storage-driver:
```
> cat /etc/docker/daemon.json
{
  "storage-driver": "btrfs"
}
```
For full list of supported drivers refer to [storage drivers](https://docs.docker.com/engine/userguide/storagedriver/selectadriver/)

### Change dockerd sockets:
```
> cat /etc/docker/daemon.json
{
        "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"]
}
```
It is possible that run init/upstart/service script specifies `-H` flag for startup command.  
This must be removed from script itself, otherwise `dockerd` will fail to start

## Underlying technology
Several linux kernel features are used by Docker.

### Namespaces
5 Linux [namespaces](https://github.com/kiemlicz/util/wiki/Containerization#namespaces) are used in Docker implementation

1. `pid`
2. `net`
3. `ipc`
4. `mnt`
5. `uts`

The `cgoup` namespace is not used.

### Control groups (`cgroups`)
Allows limiting available resources (e.g. hardware resources) for containers. For instance allows to specify available amount of memory

### Union file systems
UnionFS

### Container format
The mix of aforementioned three (namespaces, cgroups and union fs) is called the container format. The current default: `libcontainer`. This abstractions will allow other formats like BSD Jalis to be used interchangeably 

# References
 1. https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#label
 2. https://lwn.net/Articles/621006/
 3. https://www.slideshare.net/kerneltlv/namespaces-and-cgroups-the-basis-of-linux-containers
 4. https://codefresh.io/docker-tutorial/java_docker_pipeline/
 5. https://docs.docker.com/get-started/overview/
 6. https://stackoverflow.com/questions/49162358/docker-init-zombies-why-does-it-matter