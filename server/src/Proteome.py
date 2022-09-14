#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun 30th, 2022
@author: Victoria Niu
"""
 
from email.policy import default
import pandas as pd
import numpy as np
from Bio import SeqIO
import collections
from scipy import stats

class ProteomeProtein:
    def __init__(self) -> None:
        """
        self.records is a dictionary which stores the different info from .fna files
        the keys are id, name, description, sequence
        """
        self.records = collections.defaultdict() #stores the whole meta data for the fasta files
        self.tetramersFreq=collections.defaultdict(int)
        self.positions=collections.defaultdict(list)
        self.pValue=[]
    
    def readFNAFile(self, path) -> list :
        """
        SeqRecord(seq=Seq('MESLVPGFNEKTHVQLSLPVLQVRDVLVRGFGDSVEEVLSEARQHLKDGTCGLV...VNN'), 
        id='YP_009724389.1', 
        name='YP_009724389.1', 
        description='YP_009724389.1 ORF1ab polyprotein [Severe acute respiratory syndrome coronavirus 2]', dbxrefs=[])

        https://biopython.org/wiki/SeqRecord
        """
        record = list(SeqIO.parse(path, "fasta"))
        self.records['id'] = record[0].id
        self.records['name'] = record[0].name
        self.records['sequence'] = record[0]._seq
        self.records['description'] = record[0].description

    def setProtein(self, name = None, description = None,sequence = None, length = None, id = None):
        if name is not None:
            self.records['name'] = name
        if id is not None:   
            self.records['id'] = id
        if sequence is not None:
            self.records['sequence'] = sequence
        if length is not None:
            self.records['length'] = length
        if description is not None:
            self.records['description'] = description

    def setName(self, name):
        self.records['name'] = name

    def setDescription(self, descriptor):
        self.records['description'] = descriptor

    def setLength(self, length):
        self.records['length'] = length

    def setId(self, numID):
        self.records['id'] = numID

    #replade the 'X' in the protein sequence to 'Q'
    def replace(self, x):
        x=x.replace("X","Q")
        return x
    
    def countTotalTetramers(self) -> int:
        if not self.records['sequence']:
            raise Exception("Empty frequency! Please execute countFrequency() first!")
        else:
            return len(self.records['sequnce'])-3
    
    def countTetramers(self):
        """
        using sliding window to count the frequencies of tetramers and also the positions
        update self.tetramerFreq and self.positions
        """
        sequence = self.records['sequence']
        if not sequence:
            raise Exception("Empty sequence! Please be sure to execute readFNAFile()!")
        for i in range(len(sequence)-4):
            #count the frequency of tetramers in this 12 long protein
            tetramer = sequence[i:i+4]
            self.tetramersFreq[str(tetramer)]+=1
            self.positions[str(tetramer)].append(i)
        
    #calculates probability value based off a control dictionary
    #a control dictionary has a p value for each amino acid
    def calculateProbabilityTetramer(Tetramer,ControlDict):
        endValue = 1.0
        for AminoAcid in Tetramer:
            endValue = endValue * ControlDict[AminoAcid]
        return endValue

    def calculatePValue(self,expected,actual):
        """
        Use expected value and real result
        """
        a = np.array(expected)
        b = np.array(actual)

        t, p = stats.ttest_ind(a,b)

        return p

    def writeToCSV(self):
        filename = r"../OutputFiles/ProteomeOutput.csv"
        with open(filename, 'w') as f:
            for key in self.tetramersFreq.keys():
                f.write("%s,%s,%s\n"%(key,self.tetramersFreq[key],str(self.positions[key])))

    def getId(self):
        if not self.records:
            raise Exception("Empty records!")
        
        return self.records['id']
    
    def getName(self):
        if not self.records:
            raise Exception("Empty records!")
        
        return self.records['name']

    def getDescription(self):
        if not self.records:
            raise Exception("Empty records!")
        
        return self.records['description']

    def getSequence(self):
        if not self.records:
            raise Exception("Empty records!")
        
        return self.records['sequence']
    
    def getParameter(self, paramString):
        if not self.records:
            raise Exception("Empty records!")
        return self.records[paramString]
    
    #function created that takes in a list of proteome objects
    #then returns either a corresponding list of ID's, names, descriptions, etc
    #it accepts a list of proteomes and a list of strings representing parameters as an argument
    #for each string, it will compile a list of parameters of that type and put it all
    #into a list
    #ex. getMemberFromList([proteome1, proteome2, ...., proteome n], ["id, name, sequence"])
    #    returns [[p1Id, p2Id, ....], [p1Name, p2Name, ...], [p1Sequence, p2Sequence, ...]]
    def getMemberFromList(ProteomeList, parameterList):
        #2d list that we output containing all lists that we need
        OutputList = []
        for i in range(0, len(parameterList)):
            OutputList.append([])

        for proteome in ProteomeList:
            for i in range(0, len(parameterList)):
                OutputList[i].append(proteome.getParameter( ParameterList[i]) )
        return OutputList

        


    
    
