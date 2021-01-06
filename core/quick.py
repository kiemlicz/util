#!/usr/bin/env python3
import libtmux


def split_window(window, chunks, vertical=True):
    height = int(window.attached_pane.cmd("display", "-p", "#{pane_height}").stdout[0])  # first line
    for i in range(chunks - 1):
        window.split_window(attach=False, vertical=vertical)
    for pane in window.panes:
        pane.set_height(height / chunks)


def execute(pane, cmd):
    pane.send_keys(cmd)


def setup_cpu(window):
    window.rename_window("CPU/MEM")
    split_window(window, 4)
    panes = window.panes
    execute(panes[0], "vmstat -SM 1")
    execute(panes[1], "mpstat -P ALL 1")
    execute(panes[2], "pidstat 1")
    execute(panes[3], "free -m")


def setup_io(window):
    window.rename_window("IO")
    split_window(window, 3)
    panes = window.panes
    execute(panes[0], "iostat -szx 1")
    execute(panes[1], "sar -n DEV 1")
    execute(panes[2], "sar -n TCP,ETCP 1")


server = libtmux.Server()
session = server.new_session("perf")
setup_cpu(session.attached_window)
setup_io(session.new_window("IO"))
