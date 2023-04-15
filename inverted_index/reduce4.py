#!/usr/bin/env python3
"""Reduce 4."""
import sys
import itertools
import math


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    num = 0
    with open('total_document_count.txt', 'r', encoding="utf-8") as doc_file:
        num = int(doc_file.readline())
    for line in group:
        doc_id, tfi, nki = line.partition("\t")[2].split()
        idf = math.log10(float(num)/float(nki))
        wik = float(tfi) * idf
        print(f"{key}\t{doc_id} {tfi} {idf} {wik}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
