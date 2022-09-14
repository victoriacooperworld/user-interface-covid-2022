

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