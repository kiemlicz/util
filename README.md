# Basics
The "project" aims to provide scripts/functions for various tasks in day-to-day work.  
The additional rationale of this "project" is following: to encourage writing actual executable hands-on scripts/functions
instead of untested and lengthy wiki/confluence pages/blog posts/etc. containing various technical manuals.

This project does **not** aim to duplicate the functionality of command-line completions. 
Thus, one-line functions for tools with decent completions should not be here.  

Directory layout should be self-documenting about where to find which pieces.

ZSH-compliant, possibly BASH too.

Contributions are welcome.

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
In order to see full descriptions of functions adding:  
`zstyle ":completion:*:descriptions" format "%B%d%b"` to `.zshrc` may be needed

## Documentation
Please visit [wiki](https://github.com/kiemlicz/util/wiki) if you want to find out more
