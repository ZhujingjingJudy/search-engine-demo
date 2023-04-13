#!/usr/bin/env python3
"""Map 2. Calculate nk"""
import sys

for line in sys.stdin:
    doc_id, term = line.partition("\t")[0]
    tf = line.partition("\t")[2]
    print(f"{term}\t{doc_id} {tf}")