#!/home/lerathebest/.local/share/virtualenvs/Orchestration_hw-lGoKxMCX/bin/python

from Bio import SeqIO
from collections import Counter
import argparse
import json

def get_kmers(seq, k=4):
    seq = str(seq)
    for i in range(k, len(seq)+1):
        km = seq[i-k:i]
        yield km

parser = argparse.ArgumentParser(prog="Kmers count", description="Counts kmers in sequences")
parser.add_argument("--fa", help="fasta file with sequences")
args = parser.parse_args()
file = args.fa

result = dict()

for seq_record in SeqIO.parse(file, "fasta"):
    kmers = get_kmers(seq_record.seq)
    result[seq_record.id] = Counter(kmers)

print(result)

with open("out.json", "w", encoding="utf-8") as file:
    json.dump(result, file)
