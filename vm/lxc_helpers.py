#!/usr/bin/env python3

import lxc


def exists(name):
    return name in lxc.list_containers()
