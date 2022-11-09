

import csv
import datetime
import multiprocessing
import os
import sys
import logging


import GenerateDB.STetramerNRlarge as STetramerNRlarge
import GenerateDB.DatabaseInit as DatabaseInit
import itertools 
from Bio import SeqIO
"""
This function is used for divding the big file into smaller ones
The input file we used was nr.gz - a fasta file that contains almost 420 million proteins
The size is 218GB but it is too big and will cause memory issues.
This function can make the bigger files into smaller ones.

parameters:
filePath: the file path of the orginal file
outputPath: the path to save the divided files
fileSize: how many proteins are there in a file
"""


def GenerateDivideFiles(filePath, outputPath, fileSize):
    record_iterator = SeqIO.parse(filePath,"fasta")
    index = 0
    fileNum = 0
    ofile = outputPath + "\\File7" + ".fna"
    print(ofile)
    outFile = open(ofile,"w")
    try:
        while(1):
            if index %fileSize == 0 and index !=0:
                outFile.close()
                fileNum+=1
                ofile = outputPath + "\\File" + str(fileNum)+".faa"
                outFile = open(ofile,"w")
            
            curSequence = next(record_iterator)
            seq = str(curSequence._seq) 
            descript = ">" + str(curSequence.description)
            entry = descript + "\n"+seq+"\n"
            outFile.write(entry)
            index += 1
    except StopIteration:
        pass
    outFile.close()

def GenerateMergedFiles(filePath, outputPath, NumFiles):
    pass



if __name__ == '__main__':
    filePath = r"D:\DividedFilesHuman\human.7.protein.faa"
    base_address = os.path.dirname(sys.path[0])
    #filePath = f"{base_address}\\InputFiles\\NR_Data\\First200000proteins_of_nr.fna"
    outputPath = r"F:\Non-redundantProteome\Human"

    GenerateDivideFiles(filePath, outputPath, 1000000)