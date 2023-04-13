#!/usr/bin/env python3
"""maps word occurences."""
import sys

for line in sys.stdin:
    line = line.split("\t")
    content = line[1].strip()
    words = content.split("[")[1]
    words = words.split("]")[0]
    words = words.split(",")
    for word in words:
        sys.stdout.write(f"{line[0]} {word}\t1\n")
