

import csv
import datetime
import multiprocessing
import os
import sys
import logging


from GenerateDB.TetramerTableInit import initialize_database
import GenerateDB.STetramerNRlarge as STetramerNRlarge
import GenerateDB.DatabaseInit as DatabaseInit
import itertools 
from Bio import SeqIO


def generateSampleSize(filePath, outputPath, numProteins):
    record_iterator = SeqIO.parse(filePath,"fasta")
    ofile = open(outputPath, "w")
    for i in range(0,numProteins):
        curSequence = next(record_iterator)
        seq = str(curSequence._seq)
        descript = ">" + str(curSequence.description)
        entry = descript + "\n"+seq+"\n"
        ofile.write(entry)
    ofile.close()


def merge():
    inputs = []
    for file in os.listdir("D:\Human"):
        if file.endswith(".fna"):
            inputs.append(os.path.join("D:\Human", file))
 
 
    # concatanate all txt files in a file called merged_file.txt
    with open('D:\Human\merged_file.fna', 'w') as outfile:
        for fname in inputs:
            with open(fname, encoding="utf-8",  errors='ignore') as infile:
                outfile.write(infile.read())

if __name__ == '__main__':
    merge()
    # filePath = r"E:\Non-redundantProteome\nr\nr"
    # outputPath = r"..\OutputFiles"

    # generateSampleSize(filePath, outputPath, 500000)