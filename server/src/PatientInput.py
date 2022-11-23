from math import ceil
from mimetypes import init
import os
import pandas as pd
from Bio import SeqIO
import collections

import GenerateDB.STetramerNRlarge as STetramerNRlarge

CONTROL_PATH = r"InputFiles/Control.csv"
class Input:
    def __init__(self) -> None: 
        self.exportData = collections.defaultdict(list)
        self.cutoffTable = []       #a list of pairs. each element is [size, cutoffValue]

        path = CONTROL_PATH
        self.controlDict = STetramerNRlarge.readFile(path)
        self.tetDict = STetramerNRlarge.generateTetramerStr(self.controlDict)


    def getDir(self, path, outputPath = None):
        for filename in os.listdir(path):
            if filename.endswith('.fna'):
                p = path+'/'+filename
                self.readFNAFile(p, True) #returns the significant sequences
        #print(self.exportData)
        if outputPath is not None:
            self.exportCsv2(outputPath)
            
        masterList = []
        for sublist in self.exportData.values():
            for sequenceItem in sublist:
                #print(sequenceItem)
                masterList.append(sequenceItem)
        return masterList


    def readFNAFile(self, path, outputPath) -> list :
        if outputPath == None:
            print("Output path is none")
        print("HELLO")
        sequences = []
        if outputPath != None:
            output = open(outputPath, 'w')
        
        for file in os.listdir(path):
            print(file)
            with open(os.path.join(path,file),'r') as f:
                while True:
                    header = f.readline()
                    if not header:
                        break
                    sequence =f.readline()
                    sequence = sequence.replace("X","Q")
                    sequences.append([sequence.strip('\n'),int(header.split('_')[-1] )])
                #    for s in sequences:
                #         p = 1
                #         for aminoAcid in s:
                #             p *= self.tetDict(aminoAcid)
                #         # if p >= 0.05:  #chai square 
                #         #     #significant ones
                    if outputPath !=None:
                        output.write(header)
                        output.write(sequence)
        if outputPath !=None:
            output.close()

        # print(sequences)
        return sequences


    def readOneFNAFile(self, path) -> list :
        sequences = []
        
        # print(self.controlDict)
        with open(path,'r') as f:
            while True:
                p = 1
                header = f.readline()
                if not header:
                    break
                sequence =f.readline().strip('\n')
                freq = int(header.split('_')[-1])
                
                for aminoAcid in sequence:
                    p *= self.controlDict[aminoAcid]
                sequences.append([sequence,freq, p])
        # print(sequences)
        return sequences


    def exportCsv(self, outputPath):
        exportArray = []
        for fileName, sequenceList in self.exportData.items():
            for sequence in sequenceList:
                entry=[]
                entry.append(fileName)
                entry.append(sequence[0])
                entry.append(sequence[1])
                exportArray.append(entry)
        #print(exportArray)
        outputDF = pd.DataFrame(exportArray)
        outputDF.to_csv(outputPath)

    def exportCsv2(self, outputPath):

        masterArray = []
        indexes = []


        for fileName, sequenceList in self.exportData.items():
            sequenceEntries = []
            freqList = []
            indexes.append(fileName)
            indexes.append(fileName)
            for sequence in sequenceList:
                sequenceEntries.append(sequence[0])
                freqList.append(sequence[1])
            masterArray.append(sequenceEntries)
            masterArray.append(freqList)
        print(masterArray, indexes)

        index = pd.DataFrame(masterArray)
        index.transpose().to_csv(outputPath, header = indexes)

    
        





