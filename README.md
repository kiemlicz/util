#Basics
The "project" aims to provide scripts/functions for various tasks in day-to-day work.
Additional rationale of this "project" is following: to encourage writing actual executable hands-on scripts/functions
instead of untested and lengthy wiki/confluence/blog posts/etc. pages containing various technical manuals.

Directory layout should be self-documenting about where to find which pieces.

Any changes are more than welcome.

##Usage
Most common usage:
```shell
. jvm/profiling_functions
find_top_n_stacks 1234 5
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
