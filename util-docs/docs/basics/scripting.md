# Command substitution
`` `some command` `` plugs the `some command` output into some other context.
Currently backticks are deprecated in favour of `$(some command)` form which:

1. permits nesting `$(some command $(some nested))`
2. treats `\\` differently

# Process substitution
`<(command_list)` Feeds the output of processes into the _stdin_ of another process (piping allows only one
command output to be redirected into _stdin_ of another process).

The process list is run with its input or output connected to a FIFO or some file in /dev/fd.
The name of this file is passed as an argument to the current command as the result of the expansion.

# Bash
Nothing more than shell implementation

## Expansions
Controls how parameters/expressions are expanded

### Variable expansion
Introduced by `$` e.g. `$param_name`. Variable may be enclosed in braces in order to separate it from adjacent characters

### Tilde expansion
Begins with unquoted `~`, includes all following characters up to unquoted slash. Characters are treated as login name. Evaluation of `~login` yields `login` user home directory.

#### Indirect expansion
todo

### Quotes
Single quotes preserve everything. No expansion occurs

## Built-in variables
Positional parameters
* `$#` number of command line arguments
* `$*` all of positional arguments (single word)

Special
* `$?` last command's exit code
* `$!` most recently executed process ID

## Test constructs
`if` statement tests wheter exit status of _command_ is equal to 0
```
if test command; then
   #sth
fi
```
bash has alias for `test` command and is called `[` so the statement becomes:
```
if [ command ]; then
fi
```
With Bash 2.02 extended test statement was introduced:
```
if [[ command ]]; then
fi
```
Extended test statement is **not** compliant with POSIX. It features:
* No need to quote variables (in `[` not quoted variables like "something with spaces" will yield error: _too many arguments_)
* Regular expression matching with `=~` e.g. `[[ $variable =~ .*string ]]`
* Wildcard matching e.g. `[[ $(lxc-ls) == *"desired_container"* ]]`
* Chaining tests with _and_ and _or_ like: `[[ ... && ... ]]` (otherwise: `[] && []`)

### Negate
To negate test condition:
`if ! [ ... ]`
## Conditional expressions
| condition | description |
|-|-|
| `-f file` | true if file exists and is regular file |
| `-z string` | true if length of string is zero |
| `-n string` | true if length of string is non-zero |

## Exit codes
Bash scripts can exit with error codes  
Some codes have special meaning

| code | meaning |
|-|-|
| 1 | general catch-all |
| 2 | misuse of built-ins (e.g. syntax errors like missing keywords) |
| 126 | cannot execute command (permission issue or not executable script) |
| 127 | command not found (typo or command missing on `$PATH`) |
| 128 | wrong `exit` argument |
| 128+`n` | fatal signal `n` |
| 130 | termination via signal (`ctrl+c`) |


# AWK
print the quote sign
```
awk 'BEGIN { print "Here is a single quote <'"'"'>" }' #this is concat of three strings '...' "'" '...'
awk 'BEGIN { print "Here is a single quote <'\''>" }'
```
simple examples:
```
#longest line in data file
awk '{ if (length($0) > max) max = length($0) }
     END { print max }' data
# Print every line that has at least one field
awk 'NF > 0' data
```
you can have multiple rules in awk (first goes first rule, then second, if line contains both patterns then will be processed two times)
```
awk '/12/ { print $0 }
     /21/ { print $0 }' data
```
awk env variables:
 - `AWKPATH` - contains awk programs
 - `AWKLIBPATH` - contains extensions (can be written in C/C++)

# References
 1. https://google.github.io/styleguide/shell.xml
 2. https://github.com/robbyrussell/oh-my-zsh/wiki/Coding-style-guide
 3. http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html
 4. https://www.kernel.org/doc/Documentation/process/coding-style.rst
 5. https://github.com/zsh-users/zsh-completions/blob/master/zsh-completions-howto.org
 6. http://www.tldp.org/LDP/abs/html/internalvariables.html
 7. http://mywiki.wooledge.org/BashFAQ
 8. http://mywiki.wooledge.org/BashPitfalls
 9. https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
 10. http://wiki.bash-hackers.org/syntax/pe (http://wiki.bash-hackers.org/start)
 11. http://tldp.org/LDP/abs/html/exitcodes.html
 12. https://www.gnu.org/software/bash/manual/html_node/Tilde-Expansion.html