#!/home/lerathebest/anaconda3/envs/dls/bin/python
from Bio.Seq import Seq
from Bio.SeqUtils import GC
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--seq", type=str, help="dna string to process")
args = parser.parse_args()
seq = args.seq

seq_bp = Seq(seq)
rev_comp = seq_bp.reverse_complement()
gc = GC(seq_bp)

print(rev_comp)
print(gc)
