#!/usr/bin/env python3
"""Map 2. Calculate term frequency."""
import sys
import re

for line in sys.stdin:
    text = line.partition("\t")[2]
    doc_id = line.partition("\t")[0]
    text = text.split("[")[1]
    text = text.split("]")[0]
    text = re.sub(r"[,']+", " ", text)
    list_word = text.split()
    length = len(list_word)
    for i in range(length):
        print(f"{doc_id} {list_word[i]}\t1")
