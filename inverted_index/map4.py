#!/usr/bin/env python3
"""Map 4. Calculate wik."""
import sys

for line in sys.stdin:
    line = line.strip()
    term = line.partition("\t")[0]
    doc_id, tf, nk = line.partition("\t")[2].split()
    print(f"{term}\t{doc_id} {tf} {nk}")
