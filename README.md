#Basics
The "project" aims to provide scripts/functions for various tasks in day-to-day work.
Additional rationale of this "project" is following: to encourage writing actual executable hands-on scripts/functions
instead of untested and lengthy wiki/confluence/blog posts/etc. pages containing various technical manuals.
This project does **not** aim to duplicate the functionality of command-line completions. 
Thus one-line functions for tools with decent completions should not be here.  

Directory layout should be self-documenting about where to find which pieces.

Any changes are more than welcome.

##Usage
Most common usage:
```shell
> . jvm/profiling_functions
find_top_n_stacks 1234 5
```
For [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) users. Add symlink to this project:

`ln -s $UTIL_LOCATION $ZSH_CUSTOM/plugins/util`. 

This will add function `util` with auto-complete for `_function` e.g.
```shell
> util <press tab>
```

##General information
Some quick shell shortcuts&information you most likely know.
###General shell shortcuts
`ctrl + k`	cut/delete text from cursor position till the end of the line

`ctrl + u`	cut line

`ctrl + y`	paste line

`ctrl + a`	move cursor to the begining of the line

`ctrl + e`	move cursor to the end of the line

`alt + f`		move cursor one word right

`alt + b`		move cursor one word left

`ctrl + l`	cls

###Scripting
Heavily used well-known techniques.
####Command substitution
`` `some command` `` plugs the `some command` output into some other context.
Currently backticks are deprecated in favour of `$(some command)` form which:

1. permits nesting `$(some command $(some nested))`
2. treats `\\` differently

####Process substitution
`<(command_list)` Feeds the output of processes into the _stdin_ of another process (piping allows only one
command output to be redirected into _stdin_ of another process).

The process list is run with its input or output connected to a FIFO or some file in /dev/fd.
The name of this file is passed as an argument to the current command as the result of the expansion.

####References
 1. https://google.github.io/styleguide/shell.xml
 2. https://github.com/robbyrussell/oh-my-zsh/wiki/Coding-style-guide
 3. http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html
 4. https://www.kernel.org/doc/Documentation/CodingStyle
 5. https://github.com/zsh-users/zsh-completions/blob/master/zsh-completions-howto.org
 
---
#Table of contents
Enclosed operations:
 1. [Certificate](cert/README.md)
 2. [Container](container/README.md)
 3. [OS](core/README.md)
 4. [DB](db/README.md)
 5. [JVM](jvm/README.md)
 6. [Networks](net/README.md)
 7. [VM](vm/README.md)
