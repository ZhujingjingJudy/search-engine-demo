#!/usr/bin/env python3
"""Map 2. Calculate nk"""
import sys

for line in sys.stdin:
    doc_id, term = line.partition("\t")[0].split()
    # print("doc id:", doc_id)
    # print("term:", term)
    tf = line.partition("\t")[2]
    tf = tf.partition("\n")[0]
    print(f"{term}\t{doc_id} {tf}")