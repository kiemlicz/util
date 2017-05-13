# Basics
The "project" aims to provide scripts/functions for various tasks in day-to-day work.  
Additional rationale of this "project" is following: to encourage writing actual executable hands-on scripts/functions,
instead of untested and lengthy wiki/confluence pages/blog posts/etc. containing various technical manuals.

This project does **not** aim to duplicate the functionality of command-line completions. 
Thus one-line functions for tools with decent completions should not be here.  

Directory layout should be self-documenting about where to find which pieces.

Any changes are more than welcome.

## Usage
 - Most common usage:
```shell
> . jvm/profiling_functions
find_top_n_stacks 1234 5
```
 - For [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) users. Add symlink to this project:

`ln -s $UTIL_LOCATION $ZSH_CUSTOM/plugins/util`. 

This will add function `util` with auto-complete for any file ending with: `_function` e.g.
```shell
> util <press tab>
```
`util` just sources given `_functions` files so that its content is available in current shell.

---
# Table of contents  
1. General
   * [terminal and shell](https://github.com/kiemlicz/util/wiki/terminal)
   * [shell shortcuts](https://github.com/kiemlicz/util/wiki/shell)
   * [redirects](https://github.com/kiemlicz/util/wiki/redirects)
   * [editors](https://github.com/kiemlicz/util/wiki/editors)
   * [scripting](https://github.com/kiemlicz/util/wiki/scripting)
   * [GIT](https://github.com/kiemlicz/util/wiki/git)
   * [dotfiles](https://github.com/kiemlicz/util/wiki/dotfiles)
2. OS  
   * fundamentals
     * [memory](https://github.com/kiemlicz/util/wiki/memory)
     * [kernel](https://github.com/kiemlicz/util/wiki/kernel)
   * [package managment](https://github.com/kiemlicz/util/wiki/packages)
   * [crypto](https://github.com/kiemlicz/util/wiki/crypto)
   * FS
     * [BTRFS](https://github.com/kiemlicz/util/wiki/btrfs)
     * [CIFS](https://github.com/kiemlicz/util/wiki/cifs)
     * [SSHFS](https://github.com/kiemlicz/util/wiki/sshfs)
   * [unattended installation](https://github.com/kiemlicz/util/wiki/unattended)
3. Virtualization
   * [VM](https://github.com/kiemlicz/util/wiki/vm)
   * [Lightweight VM](https://github.com/kiemlicz/util/wiki/Containerization)
4. Networks
   * [configuration](https://github.com/kiemlicz/util/wiki/netcfg)
   * [traffic dumping](https://github.com/kiemlicz/util/wiki/traffic)
   * Protocols&Implementations
     * [SSH](https://github.com/kiemlicz/util/wiki/ssh)
     * [SSL](https://github.com/kiemlicz/util/wiki/ssl)
5. Infrastructure as a code
   * [Foreman](https://github.com/kiemlicz/util/wiki/Foreman)
   * [SaltStack](https://github.com/kiemlicz/util/wiki/saltstack)
6. Desktop environments
   * [KDE](https://github.com/kiemlicz/util/wiki/kde)
   
# Handy cheat sheet

![](http://brendangregg.com/Perf/linux_perf_tools_full.png)
