#Basics
This section contains most generic set of functions to be used for text operations/os operations

##Environment variables
Shell can have two types of variables:
 - local: accessible only via current shell. Created: `a=some_value`. Displayed with `set` command
 - exported: passed to every child process. Created: `export a=some_value`. Displayed with `env` command

##Package management
Useful information about different package managers
###APT/Aptitude
Highest priority number means highest priority of package.
 
Show available/installed package version:

`aptitude versions the_package` or `dpkg-query -l | grep the_package`

Upgrade/downgrade only one specific package:

`apt-get install --only-upgrade the_package`

Remove dangling packages:

`apt-get autoremove --purge`

Remove old cached packages:

`aptitude autoclean`

Remove cached packages:

`aptitude clean` 
####Preferences
Mechanism that determines which version of the package will be installed (consult: `man apt_preferences`).

Used to pick **package version** when _apt list files_ (`/etc/apt/sources.list` or `/etc/apt/sources.list.d/*.list`) contains references to more than one distribution eg. contains both stable and testing repositories. 
 1. Normally without using apt_preferences the apt will pick the package coming from the first entry in `sources.list`.
 2. If no preferences exists or contains no entry for given package then the package priority is the priority of distro.
 3. To “force” usage of some other distro, use `-t` flag (specify target release), eg. 
`apt-get install -t experimental some-package`. If `-t` is given then check man `apt_preferences` for algorithm that assign priority for package. 
It roughly specifies:
    - If target release contains in release files _“NotAutomatic: yes”_ but not _“ButAutomaticUpgrades: yes”_. Then the priority is 1
    - If package is installed or if target release’s release file contains _“NotAutomatic: yes”_ and _“ButAutomaticUpgrades: yes”_. Then the priority is 100
    - If the package is not installed and do not belong to the target release. Then the priority is 500
    - If the package is not installed and belong to the target release. Then the priority is 990
    
Please mind that if you have configured package pinning and e.g. your stable is configured to have priority of 995 (or anything greater than 990) then `-t` will have **no effect**.

You can always verify with `apt-cache policy -t target-release package` which exact version of package is going to be installed
 4. Installs version with highest priority (highest number).

##OS monitoring
Useful information about common tools to monitor e.g. RAM

`free (-m to show in MB)`
 - total: indicates memory/physical RAM available for your machine. By default these numbers are in KB's.
 - used: indicates memory/RAM used by system. This includes buffers and cached data size as well.
 - free: indicates total **unused** RAM available for new process to run.
 - shared:  indicates shared memory. This column is obsolete and may be removed in future releases of free.
 - buffers: indicates total RAM buffered by different applications in Linux
 - cached: indicates total RAM used for Caching of data for future purpose
 - -/+ buffers/cache: shows _used_ column minus (_buffers_+_cached_) and _free_ column plus (_buffers_+_cached_). 
 Why is that? Because when memory used is getting up to limit, the buffers + cache will be freed and used by demanding applications. 
 This show most accurate memory usage.
 
New version of `free`:
 - buff/cache: sum of buffers and cached
 - available: not exactly _free_ column plus (_buffers_+_cached_)
