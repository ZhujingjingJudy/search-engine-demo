#!/usr/bin/env python3
"""
Reduce 1.
"""
import sys
import itertools
import re


def reduce_one_group(key, group):
    """Reduce one group."""
    combined =""
    for line in group:
        txt = line.partition("\t")[2]
        title = txt.partition("\t")[0]
        body = txt.partition("\t")[2]
        combined = title + " " + body
        combined = re.sub(r"[^a-zA-Z0-9 ]+", "", combined)
        combined = combined.casefold()
        combined = combined.split()
        with open('stopwords.txt', 'r') as word_file:
            stop_words = [line for line in word_file]
        combined = [term for term in combined if term not in stop_words]
    print(f"{key}\t{combined}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()