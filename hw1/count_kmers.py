#!/home/lerathebest/.local/share/virtualenvs/Orchestration_hw-lGoKxMCX/bin/python

from Bio import SeqIO
from collections import Counter
import argparse
import json

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

result = dict()

for seq_record in SeqIO.parse(file, "fasta"):
    kmers = get_kmers(seq_record.seq, k)
    result[seq_record.id] = Counter(kmers)

print(result)

with open(outfile, "w", encoding="utf-8") as file:
    json.dump(result, file)
