#!/usr/bin/env python3

from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction 
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, 
    filename="complement.log",
    filemode="w")

parser = argparse.ArgumentParser(description="My script to get reverse complement dna strand and gc fraction")
parser.add_argument("--seq", type=str, help="dna string to process")
args = parser.parse_args()
seq = args.seq

seq_bp = Seq(seq)
logging.info(f"Running complement.py on {seq_bp}")

rev_comp = seq_bp.reverse_complement()
logging.info(f"Reverse complement: {rev_comp}")

gc = gc_fraction(seq_bp)
logging.info(f"GC-fraction: {gc:.3f}")

print(rev_comp)
print(f"{gc:.3f}")
