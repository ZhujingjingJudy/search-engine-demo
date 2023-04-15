#!/usr/bin/env python3
"""Map 0."""
import sys
import csv

csv.field_size_limit(sys.maxsize)
for line in csv.reader(sys.stdin):
    # doc_id, doc_ti, doc_bo = line
    print("one_doc\t1")
