#!/usr/bin/env python3
"""Reduce 5."""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    norfac = 0
    for line in group:
        term, tfi, idf, wik = line.partition("\t")[2].split()
        norfac += float(wik) ** 2
    for line in group:
        term, tfi, idf, wik = line.partition("\t")[2].split()
        print(f"{term}\t{idf} {key} {tfi} {norfac}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
