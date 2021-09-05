# Packages
Typically packages are nothing more that some kind of archive. However this archive besides the actual files to be copied to the underlying system
contains a lot of additional configuration scripts. 

## [DEB](https://github.com/kiemlicz/util/blob/master/core/deb_functions)
_AR_ archive with following 3 top-level files included:
 1. _control.tar.gz_ - control files. Theoretically it must contain following files:
  - _control_ kind of key-value file. Contains information about packaged data (like: author, some description, dependencies)  
    Fields (some of them):  
    `Source` - name of the source package  
    `Package` - name of the binary package  
    `Section` - mainly for front-ends that display packages grouped into categories  
    `Priority` - how important for the user the package is. For front-ends use (mainly when the `apt`-like software selects default packages for user or solves conflicts)  
    `Architecture` - if this package is architecture dependent (`any`) or not (`all` - e.g. Java applications)  
    `Depends` - the package will not be installed unless the packages it depends on are installed  
  - _changelog_ `dpkg` uses this files to obtain version information, distribution, urgency etc of the package 
  - _copyright_ copyright and license  
  Some of optional files:  
  - `conffiles` list of packaged application configuration files. When **upgrading** package you'll be asked what to do with any file listed here
  that changed on the filesystem  
  - `package.cron.*` e.g. `my_app.cron.hourly` will be installed as `/etc/cron.hourly/my_app` and will run every hour
  - `dirs` specifies any directories which we need but which are not created by the normal installation procedure
  - `md5sums` used to verify if installed files have been modified
 2. _data.tar.gz_ (since Debian 8: _data.tar.xz_) - actual files 
 3. _debian-binary_

## RPM
todo

# APT/Aptitude
Highest priority number means highest priority of package.

## Cheat sheet
 
| command | description |
|-|-|
| `aptitude versions the_package`, `apt-cache policy the_package`, `dpkg-query -l \| grep the_package` | show available/installed package version |
| `apt-cache depends the_package`| show package dependencies | 
| `apt-get install --only-upgrade the_package` | upgrade/downgrade only one specific package |
| `apt-get autoremove --purge` | Remove dangling packages |
| `aptitude autoclean` | remove old cached packages |
| `aptitude clean` | remove cached packages |
| `dpkg -S /bin/ping` | show to which package does the file belong to |

## Configuration
APT configuration can be dumped with:  
`apt-config dump`

To reload configuration changes (either repositories changes or `apt.conf.d/*` changes use:  
`apt-get update`

## Preferences
In general, same package may be defined in multiple repositories with different versions (or not).   
The mechanism that determines which package version will be installed is called _preferences_ (consult: `man apt_preferences`).  

Used to pick **package version** when _apt list files_ (`/etc/apt/sources.list` or `/etc/apt/sources.list.d/*.list`) contains references to more than one distribution eg. contains both stable and testing repositories. 
 1. Normally without using apt_preferences the apt will pick the package coming from the first entry in `sources.list`.
 2. If no preferences exists or contains no entry for given package then the package priority is the priority of distro. If preference exists for given package then its value is used.
 3. To “force” usage of some other distro, use `-t` flag (specify target release), eg. 
`apt-get install -t experimental some-package`. If `-t` is given then check man `apt_preferences` for algorithm that assign priority for package. 
It roughly specifies:
    - If target release contains in release files _“NotAutomatic: yes”_ but not _“ButAutomaticUpgrades: yes”_. Then the priority is 1
    - If package is installed or if target release’s release file contains _“NotAutomatic: yes”_ and _“ButAutomaticUpgrades: yes”_. Then the priority is 100
    - If the package is not installed and do not belong to the target release. Then the priority is 500
    - If the package is not installed and belong to the target release. Then the priority is 990.
 4. Installs version with highest priority (highest number).

Please mind that if you have configured package pinning and e.g. your stable is configured to have priority of 995 (or anything greater than 990) then `-t` will have **no effect**.

You can always verify with `apt-cache policy -t target-release package` which exact version of package is going to be installed

### Override preferences
The package is **always installed** when package version (or target repository) is provided.  
To provide version use `=` e.g. `apt-get install firefox-esr=60.6.1esr-1~deb9u1`  
To provide target repository use forward slash `\ ` e.g. `apt-get install firefox-esr/stretch-updates`

### Preferences files
Located in `/etc/apt/preferences.d`  
Parsed in alphanumeric ascending order  

Need to obey convention: 
 1. No filename extension or `.pref`
 2. Filename chars allowed: alphanumeric, hyphen, underscore and period

The file itself contains records separated by blank lines.  
Preference refers to the mentioned package(s) and the mentioned package(s) only (doesn't affect its dependencies).  
This is one of the reasons why this mechanism is kind of "discouraged".  
Typical `pref` file:
```
Package: *
Pin: release o=Debian,a=testing
Pin-Priority: 900
```
Configuration options:

| Option | Meaning |
|-|-|
| `Pin-Priority` | The priority |
| `Package` | To which package does the rule apply to. Can be regex |
| `Pin` | More complex rule to match packages on. Using `Pin` it is possible to point the desired repository that will be used to fetch package |

#### Pin
Possible `Pin` options (and they should be defined) are rather poorly documented.  
Using `Pin` it is possible to point the exact repository to be used for given package(s).  

##### Pin to version
Without regards to repository holding the `perl` package, this `Pin` will assign 1001 priority to every `perl` package version matching `5.8*` 
```
Package: perl
Pin: version 5.8*
Pin-Priority: 1001
```

##### Pin to origin
Assiging the priority by the repository URL only.
```
Package: *
Pin: origin ftp.de.debian.org
Pin-Priority: 980
```

##### Pin to Release file
To get the values that it is possible **to pin to**, download the desired repository's `Release` file, e.g.:
```
Archive: Debian_9.0
Codename: Debian_9.0
Origin: obs://build.opensuse.org/isv:ownCloud:desktop/Debian_9.0
Label: isv:ownCloud:desktop
Architectures: amd64
Date: Thu Mar 21 19:36:06 2019
Description: qt depenendencies for client 2.5.x (Debian_9.0)
MD5Sum:
...
SHA1:
...
SHA256:
...
```
In order to use `Origin` field:
```
Package: *
Pin: release o=obs://build.opensuse.org/isv:ownCloud:desktop/Debian_9.0
Pin-Priority: 995
```
The fields:

| Release file field | Pin option |
|-|-|
| `Archive`, `Suite` | `a` |
| `Codename` | `n` |
| `Version` | `v` |
| `Component` | `c` |
| `Origin` | `o` |
| `Label` | `l` |

Entries can be concatenated with `,` e.g.: `Pin: release o=Debian Mozilla Team,c=iceweasel-aurora`

In order to debug what package version is going to be installed use: `apt-cache policy the_package`

## Package configuration
To display package configuration files use:  
`debconf-show the_package`

To set package configuration option use (wireshark example, using here-string):  
`debconf-set-selections <<< 'wireshark-common wireshark-common/install-setuid boolean false'`

# References
1. https://wiki.debian.org/AptPreferences
2. https://wiki.debian.org/UnattendedUpgrades
3. https://www.debian.org/doc/manuals/repository-howto/repository-howto
4. https://dug.net.pl/tekst/163/priorytety_pakietow_(apt_pinning__pin_priority)/
5. https://www.debian.org/doc/manuals/maint-guide/index.en.html
6. https://www.debian.org/doc/debian-policy/index.html