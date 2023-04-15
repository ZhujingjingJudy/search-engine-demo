#!/usr/bin/env python3
"""Reduce 3."""
import sys
import itertools
import collections


def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    # print("Group:", group)
    doc_appearence = collections.defaultdict(int)
    for line in group:
        doc_id, tf_index = line.partition("\t")[2].split()
        doc_appearence[doc_id] += 1
    nk_index = len(doc_appearence)

    # for dic_items in doc_appearence.items():
    #     nk_index += 1
    for line in group:
        doc_id, tf_index = line.partition("\t")[2].split()
        print(f"{key}\t{doc_id} {tf_index} {nk_index}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    # print(line.partition("\t")[0])
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
