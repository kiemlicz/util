# Terminal/Console
Execution environment for applications. Provided by the kernel. Usually provides the hardware (keyboard).

Exposes text buffer. Only one application runs in foreground (this application "owns" keyboard/mouse).

# Shell
Application. The command interpreter.

## Shortcuts
- `ctrl + k` cut/delete text from cursor position till the end of the line
- `ctrl + u` cut line
- `ctrl + y` paste line
- `ctrl + a` move cursor to the begining of the line
- `ctrl + e` move cursor to the end of the line
- `alt + f` move cursor one word right
- `alt + b` move cursor one word left
- `ctrl + l` clear screen
- `alt + .` last command's argument

Uses terminal, exposes OS functionality for user (via commands). Allows configuration of execution environment (via variables)

## Redirections
In fact: duplicating  
When anything like `2>&1` is encountered, it means that anything that descriptor 2 contains is copied to descriptor 1, thus the order of "redirects" matter:

`ls / not_existing_file 2>&1 1>/dev/null` - the `stderr` is copied to whatever the descriptor 1 points to (`stdout` by default), the `stdout` is copied to `/dev/null`, the `stderr` is not updated

`ls / not_existing_file 1>/dev/null 2>&1` - the `stdout` is copied to `/dev/null` the `stderr` is copied to whatever the descriptor 1 points to (`dev/null` in this case)

### Closing file descriptors
To close descriptor, duplicate `-`, e.g.:  
Close stdin: `0<&-`  
Close stdout: `1<&-`

# Environment variables
Shell utilizes two types of variables:
- _local_: accessible only via current shell. Not passed to child processes. Created: `a=some_value`.  
  Displayed with `set` command
- _exported_: passed to every child process. Created: `export a=some_value`.  
  Displayed with `env` command

# Dotfiles
This term refers to all (some will argue that not only) user local hidden files (like your _.vimrc_).  
At some point management of these file becomes cumbersome.  
There are a lot of techniques to aid this problem, personally I found one to be [particularly good](https://developer.atlassian.com/blog/2016/02/best-way-to-store-dotfiles-git-bare-repo/).


# References
1. https://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con
1. http://mywiki.wooledge.org/SignalTrap
1. https://wiki.bash-hackers.org/howto/redirection_tutorial
1. https://developer.atlassian.com/blog/2016/02/best-way-to-store-dotfiles-git-bare-repo/