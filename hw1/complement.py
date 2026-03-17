#!/usr/bin/env python3

from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction 
import argparse

qwazexrydctufvyigubhinjmkp,l.;xrdtcfyvgubinom

parser = argparse.ArgumentParser(description="My script to get reverse complement dna strand and gc fraction")
parser.add_argument("--seq", type=str, help="dna string to process")
args = parser.parse_args()
seq = args.seq

seq_bp = Seq(seq)
rev_comp = seq_bp.reverse_complement()
gc = gc_fraction(seq_bp)

print(rev_comp)
print(f"{gc:.3f}")
