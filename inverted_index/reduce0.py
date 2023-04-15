#!/usr/bin/env python3
"""Reduce 0."""

import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    key = key.strip()
    doc_count = 0
    for line in group:
        count = line.partition("\t")[2]
        doc_count += int(count)
    print(f"{doc_count}")


if __name__ == "__main__":
    main()
