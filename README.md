#Basics
The "project" aims to provide scripts/functions for various tasks in day-to-day work.
Additional rationale of this "project" is following: to encourage writing actual executable hands-on scripts/functions
instead of untested and lengthy wiki/confluence/blog posts/etc. pages containing various technical manuals.
This project does **not** aim to duplicate the functionality of command-line completions. 
Thus one-line functions for tools with decent completions should not be here.  

Directory layout should be self-documenting about where to find which pieces.

Any changes are more than welcome.

##Usage
 - Most common usage:
```shell
> . jvm/profiling_functions
find_top_n_stacks 1234 5
```
 - For [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) users. Add symlink to this project:

`ln -s $UTIL_LOCATION $ZSH_CUSTOM/plugins/util`. 

This will add function `util` with auto-complete for `_function` e.g.
```shell
> util <press tab>
```
`util` just sources given `_functions` file so that its content is available in current shell.

---
#Table of contents
[Introduction&beyond](https://github.com/kiemlicz/util/wiki)

Enclosed operations:
 1. [Certificate](cert/README.md)
 2. [Configuration management](cfg_management/README.md)
 3. [Container](container/README.md)
 4. [OS](core/README.md)
 5. [DB](db/README.md)
 6. [JVM](jvm/README.md)
 7. [Networks](net/README.md)
 8. [VM](vm/README.md)
