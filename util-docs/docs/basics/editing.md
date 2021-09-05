To set per-user default editor use `EDITOR` environmental variable.
Legend

|symbol|meaning|
|-|-|
|`C`|Control key|
|`M`|Alt key|

# Vim
In order to set options permanently, append them to `~/.vimrc`
## Edition
| operation | shortcut |
|-|-|
|cut/copy/paste|select with `v` (whole line with `V`, rectangular blocks with `ctrl + v`), use cursors, copy with `y`, cut with `d`, paste before cursor with `P`, after with `p`|
| undo | `u` |
| reformat code | `=`, e.g. `gg=G` |

## Syntax options
| option | shortcut |
|-|-|
|highlight|`:syntax on/off`|
|line numbers|`:set number` / `set nonumber`|

# Vi
## General options
| option | shortcut |
|-|-|
|compatibility mode (compatibility with very old plain _vi_), following command disables compatibility|`:set nocompatible`|

# Tmux
## Shortcuts
Assuming `C-b` is the prefix

| option | shortcut |
|-|-|
|bring tmux command line| `C-b` `:`|
|synchronize panes| `C-b` `:setw synchronize-panes` |
|align panes| vertical: `C-b` `M-2`, horizontal: `C-b` `M-1` |

# References
1. http://vim.wikia.com/wiki/Vim_Tips_Wiki
2. https://gist.github.com/MohamedAlaa/2961058