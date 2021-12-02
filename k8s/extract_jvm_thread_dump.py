#!/usr/bin/env python3

import collections
import fileinput
import re
from pathlib import Path

start = re.compile("^(\d{4}-\d{1,2}-\d{1,2}\s+\d+:\d+:\d+)\s+Full\s+thread\s+dump\s+OpenJDK.*$")
end = re.compile("^Heap[\s\S]*?(?=\n\s*\n)$", re.MULTILINE)
stdin = fileinput.input()
start_finder = collections.deque(maxlen=2)
end_finder = collections.deque(maxlen=10)  # "Heap" + some last lines


def find(lines):
    dump = []
    for line in lines:
        start_finder.append(line)
        try:
            m = start.match("".join(start_finder))
            if m:
                ts = m.group(1)
                dump.extend(start_finder)
                while not end.search("".join(end_finder)):
                    l = next(lines)
                    dump.append(l)
                    end_finder.append(l)
                return ts, dump
        except StopIteration:
            print("no thread dump end mark found")
            return None, None
    return None, None


Path("/tmp/jvm_td").mkdir(parents=True, exist_ok=True)

ts, d = find(stdin)
while d:
    with open(f'/tmp/jvm_td/dump.{ts.replace(" ", "_")}', "w") as f:
        f.write("".join(d))
    ts, d = find(stdin)
