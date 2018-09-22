#!/bin/zsh

# $1 functions type
util() {
    local util_path=$ZSH_CUSTOM/plugins/util
    source $util_path/${1}
    if [ -f $util_path/${1}_compdef ]; then
        source $util_path/"${1}_compdef"
    fi
}
