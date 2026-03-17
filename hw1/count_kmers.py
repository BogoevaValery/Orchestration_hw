#!/usr/bin/env python3

from Bio import SeqIO
from collections import Counter
import argparse
import json
import logging
import time
from datetime import datetime

start = time.time()
now = datetime.now()

logging.basicConfig(
    level=logging.INFO, 
    filename="count_kmers.log",
    filemode="w",
    format='%(message)s', 
    )

def get_kmers(seq, k):
    # kmers generator 
    seq = str(seq)
    for i in range(k, len(seq)+1):
        km = seq[i-k:i]
        yield km

parser = argparse.ArgumentParser(prog="Kmers count", description="Counts kmers in sequences")
parser.add_argument("--fa", required=True, help="fasta file with sequences")
parser.add_argument("-k", type=int, default=4, help="lenght of kmer")
parser.add_argument("--out", default="coutnt_kmers_out.json", help="output file name")

args = parser.parse_args()
file = args.fa
k = args.k
outfile = args.out
if args.out == None:
    basename = file.split(".")[0]
    outfile = f"{basename}_count_kmers.json"
else:
    outfile = args.out

logging.info(f"{datetime.strftime(now, "%d.%m.%y %H:%M:%S")}")
logging.info(f"Running count_kmers.py on file {file}")
result = dict()

cnt = 0
for seq_record in SeqIO.parse(file, "fasta"):
    kmers = get_kmers(seq_record.seq, k)
    result[seq_record.id] = Counter(kmers)
    logging.info(f"Sequence processed: {seq_record.id}")
    cnt+=1
logging.info(f"Number of sequences processed: {cnt}")

print(result)

with open(outfile, "w", encoding="utf-8") as file:
    json.dump(result, file)

end = time.time()
work_time = (end - start) * 1e3
logging.info(f"Working time: {work_time} ms")
