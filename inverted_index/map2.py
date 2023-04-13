#!/usr/bin/env python3
"""Map 2. Calculate term frequency"""
import sys

for line in sys.stdin:
    doc_id, list_word = line
    length = len(list_word)
    for i in range(length):
        print(f"{doc_id} {list_word[i]}\t1")