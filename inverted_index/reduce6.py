#!/usr/bin/env python3
"""Reduce 6."""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    key = key.strip()
    group = list(group)
    lines = []
    for line in group:
        lines.append(line.partition("\t")[2])
    sorted_lines = sorted(lines, key=lambda x: x.split()[0])
    curr_term = ""
    idf = 0
    doc_tuple_list = []
    for line in sorted_lines:
        line = line.strip()
        if curr_term == "":
            curr_term = line.split()[0]
            idf = float(line.split()[1])
            doc_tuple_list.append((line.split()[2],
                                   line.split()[3], line.split()[4]))
        elif curr_term == line.split()[0]:
            doc_tuple_list.append((line.split()[2],
                                   line.split()[3], line.split()[4]))
        elif curr_term != line.split()[0]:
            sort_doc_tu = sorted(doc_tuple_list, key=lambda x: x[0])
            print(f"{curr_term} {idf}", end="")
            for doc_tu in sort_doc_tu:
                print(f" {doc_tu[0]} {doc_tu[1]} {doc_tu[2]}", end="")
            print("\n", end="")
            curr_term = line.split()[0]
            idf = float(line.split()[1])
            doc_tuple_list = [(line.split()[2],
                               line.split()[3], line.split()[4])]
    sort_doc_tu = sorted(doc_tuple_list, key=lambda x: x[0])
    print(f"{curr_term} {idf}", end="")
    for doc_tu in sort_doc_tu:
        print(f" {doc_tu[0]} {doc_tu[1]} {doc_tu[2]}", end="")
    print("\n", end="")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
