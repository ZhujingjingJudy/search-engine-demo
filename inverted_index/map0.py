#!/usr/bin/env python3
"""Map 0."""
import sys
import csv

for line in csv.reader(sys.stdin):
    # doc_id, doc_ti, doc_bo = line
    print(f"one_doc\t1")
