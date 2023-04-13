#!/usr/bin/env python3
"""Map 5. Calculate |di|"""
import sys

for line in sys.stdin:
    term = line.partition("\t")[0]
    doc_id, tf, idf, wik = line.partition("\t")[2]
    print(f"{doc_id}\t{term} {tf} {idf} {wik}")