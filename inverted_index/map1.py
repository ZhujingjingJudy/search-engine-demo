#!/usr/bin/env python3
"""Map 1."""
import sys
import csv

csv.field_size_limit(sys.maxsize)
for line in csv.reader(sys.stdin):
    doc_id, doc_title, doc_body = line
    print(f"{doc_id}\t{doc_title}\t{doc_body}")
