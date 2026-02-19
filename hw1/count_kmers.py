#!/home/lerathebest/.local/share/virtualenvs/Orchestration_hw-lGoKxMCX/bin/python

from Bio import SeqIO

for sec_record in SeqIO.parse("test1.fa"):
    print(secrecord.id)
    print(repr(seq_record.seq))
    print(len(seq_record))
    print()
