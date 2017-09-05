#!/usr/bin/env python3

import re
import sys
from subprocess import check_output as cmd
from multiprocessing import Pool

COMPONENT = r"[\.a-zA-Z0-9-_\$]*"
SPACE_OR_NEWLINE = r"[ \n]*"
HEX_NUM = r"0x[a-zA-Z0-9]*"
OBJECT = r"[/a-zA-Z0-9-_\.]*"

LINE_ITEM = re.compile("({cmp}){sp}({hn}){sp}({hn}){sp}({obj})".format(
    cmp=COMPONENT,
    sp=SPACE_OR_NEWLINE,
    hn=HEX_NUM,
    obj=OBJECT))

DEMANGLEABLE = re.compile("(_ZN{cmp}E)".format(
    cmp=COMPONENT))

NODE_ITEM = re.compile("(<.*>|{cmp})".format(
    cmp=COMPONENT))

with open(sys.argv[1], 'r') as ifile:
    lines = ifile.read()

print("matching...")
matches = [m for m in LINE_ITEM.findall(lines)]

print("filtering removed components...")
active_items = [m for m in matches if (int(m[1], 16) != 0 and int(m[2], 16) != 0)]

print("demangling symbols...")

# p = Pool()

def demangle(i):
    component, position, size, symbol = i

    srch = DEMANGLEABLE.search(component)

    if srch != None:
        c = cmd(["c++filt", srch.group(1)]).strip().decode('ascii')
        return (c, position, size, symbol)
    else:
        return None

demangled_or_none = [demangle(d) for d in active_items]
processed_names = [d for d in demangled_or_none if d != None]

class SizeNode(object):
    def __init__(self):
        self.children = {}
        self.matches = []

    def add(self, component, addr, size):
        if len(component) == 1:
            self.matches.append((addr, size, component[0]))
            return

        if component[0] not in self.children:
            self.children[component[0]] = SizeNode()

        self.children[component[0]].add(component[1:], addr, size)

total_map = SizeNode()

for p in processed_names:
    components = [y for y in NODE_ITEM.findall(p[0]) if len(y) != 0]
    total_map.add(components, p[1], p[2])

def recursive_print(node, space=0):
    size = 0
    strs = []

    if len(node.children) == 0:
        for m in node.matches:
            strs.append("{}item:{} size:{} loc:{}".format(' ' * space, m[2], m[1], m[0]))
            size += int(m[1], 16)
    else:
        for key in sorted(node.children.keys()):
            n_size, n_strs = recursive_print(node.children[key], space+4)
            strs.append("{}{} - {}".format(' ' * space, key, n_size))
            strs.extend(n_strs)
            size += n_size

    return (size, strs)


size, strs = recursive_print(total_map)

print("Total size: {}".format(size))
for s in strs:
    print(s)
