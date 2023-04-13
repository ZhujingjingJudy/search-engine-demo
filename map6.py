#!/usr/bin/env python3
"""Map 6. segment"""
import sys

for line in sys.stdin:
    term = line.partition("\t")[0]
    idf, doc_id, tf, nocfac = line.partition("\t")[2]
    seg_id = doc_id % 3
    print(f"{seg_id}\t{term} {idf} {doc_id} {tf} {nocfac}")