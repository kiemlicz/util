#Basics
Some quick shell shortcuts&information you most likely know.
##General shell shortcuts
 - `ctrl + k` cut/delete text from cursor position till the end of the line
 - `ctrl + u` cut line
 - `ctrl + y` paste line
 - `ctrl + a` move cursor to the begining of the line
 - `ctrl + e` move cursor to the end of the line
 - `alt + f` move cursor one word right
 - `alt + b` move cursor one word left
 - `ctrl + l` clear screen
 - `alt + .` last command's argument
##Scripting
Heavily used and well-known techniques.
###Command substitution
`` `some command` `` plugs the `some command` output into some other context.
Currently backticks are deprecated in favour of `$(some command)` form which:

1. permits nesting `$(some command $(some nested))`
2. treats `\\` differently

###Process substitution
`<(command_list)` Feeds the output of processes into the _stdin_ of another process (piping allows only one
command output to be redirected into _stdin_ of another process).

The process list is run with its input or output connected to a FIFO or some file in /dev/fd.
The name of this file is passed as an argument to the current command as the result of the expansion.

#References
 1. https://google.github.io/styleguide/shell.xml
 2. https://github.com/robbyrussell/oh-my-zsh/wiki/Coding-style-guide
 3. http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html
 4. https://www.kernel.org/doc/Documentation/CodingStyle
 5. https://github.com/zsh-users/zsh-completions/blob/master/zsh-completions-howto.org
 