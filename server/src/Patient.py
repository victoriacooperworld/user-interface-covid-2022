#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun 24th, 2022
@author: Victoria Niu
"""

import csv
from mimetypes import init
import os
import pandas as pd
import numpy as np
from Bio import SeqIO
import collections
from pip import main
from scipy import stats
from statsmodels.sandbox.stats.multicomp import multipletests

class TetramerInfo:
    def __init__(self) -> None:
        self.sequence = ''
        self.freq = 0
        self.prob = 0
        self.expected  = 0 #expected = prob * totalFreq
        self.pValue =  0
        self.pBonferroni = 0
        self.pBH = 0

#takes form of tetramer info
def CompareTetramers(Tet):
        return Tet[1].freq

class PatientProtein:
    def __init__(self, data) -> None:

        if type(data) != list:
            raise Exception("ERROR IN PatientProtein OBJECT: Data type is not a 2d list")
        self.records = data #records receive the input 2d array [sequence,frequency]
        
        self.tetramers=collections.defaultdict(TetramerInfo)

    #replade the 'X' in the protein sequence to 'Q'
    def replace(self, x: str):
        x=x.replace("X","Q")
        return x
    
    def countTetramers(self):
        if not self.records:
            raise Exception("ERROR IN PatientProtein OBJECT: Empty records, something went wrong with initialization!")
        for record in self.records:
            #count the frequency of tetramers in this 12 long protein
            protein, count = record[0], record[1]
            for i in range(len(protein)-3):
                tetramer = protein[i:i+4]
                self.tetramers[tetramer].freq+=count
                self.tetramers[tetramer].sequence = tetramer
    def printTetramers(self):
        if not self.tetramers:
            raise Exception("Error in printtetramers: empty tetramer dict")
        for tetramer, tetInfo in self.tetramers.items():
            print(tetramer, " Frequency:" , tetInfo.freq)

    def countTotalTetramers(self) -> int:
        if not self.tetramers:
            raise Exception("ERROR IN PatientProtein OBJECT: Empty tetramer dict! Please execute countTetramers() first!")
        else:
            #return sum(self.tetramers.values())
            sum = 0
            for tet in self.tetramers.values():
                sum  = sum + int(tet.freq)
            return sum

    def calculateExpectedNumber(self):
        for t, info in self.tetramers.items():
            self.tetramers[t].expected = info.prob * info.freq

    
        
    #def calculatePValue(self):
    #    """
    #    Use expected value and real result
    #    Return value is an array (or float)
    #    """
    #    #actual =[]
    #    #expected=[]
    #    #
    #    #for t in self.tetramers:
    #    #    actual.append(self.tetramers[t].freq)
    #    #    expected.append(self.tetramers[t].expected)
    #    #
    #    #a = np.array(expected)
    #    #b = np.array(actual)
    #    #t, p = stats.ttest_ind(a,b)
    #    #i = 0
    #    #for t in self.tetramers:
    #    #    #update the p value
    #    #    self.tetramers[t].pValue = p[i]
    #    #    i+=1
    #    #return p

    #this static method accepts two instances of PatientProtein objects and runs binomial test on them
    @staticmethod
    def calculateOddsRatio(diseasedPopulation, nonDiseasedPopulation) -> dict:

        #getting tetramers that show up in both populations
        totalKeys = list(set(diseasedPopulation.tetramers.keys()) & set(nonDiseasedPopulation.tetramers.keys()))
        dDict = diseasedPopulation.tetramers
        ndDict = nonDiseasedPopulation.tetramers
        
        dTotFreq = diseasedPopulation.countTotalTetramers()
        ndTotFreq = nonDiseasedPopulation.countTotalTetramers()
        ratioList = {}
        for tet in totalKeys:
            #calculating via odds ratio
            #has disease and the tetramer
            topLeft = dDict[tet].freq
            topRight = ndDict[tet].freq
            botLeft = dTotFreq
            botRight = ndTotFreq
            oddsRatio = (topLeft * botRight) / (topRight * botLeft)
            ratioList[tet] = oddsRatio
        #print("Compelte")
        #print(ratioList)
        return ratioList



            
    def countTotalSequences(self):
        if not self.records:
            raise Exception("ERROR in CountTotalSequences: Self.records doesnt exist")
        sum = 0
        for sequence, frequency in self.records:
            sum+= frequency
        return frequency

    def bonferroniCorrection(self, pvals):
        bonferroni = multipletests(pvals, alpha=0.05, method='bonferroni', is_sorted=False, returnsorted=False)
        i = 0
        bonferroni = bonferroni[1]
        print(bonferroni)
        for t in self.tetramers:
            #update the p value
            self.tetramers[t].pBonferroni = bonferroni[i]
            i+=1
        
    def benjamini_hochbergCorrection(self, pvals):
        bh = multipletests(pvals, alpha=0.05, method='fdr_bh', is_sorted=False, returnsorted=False)
        i = 0
        bh = bh[1]
        for t in self.tetramers:
            #update the p value
            self.tetramers[t].pBH = bh[i]
            i+=1



    def CreateSortedTetramers(self):
        toSort =  self.tetramers.items()
        toSort = sorted(toSort, reverse = True, key = CompareTetramers)
        return toSort


    def writeToCSV(self, outputPath, sortOutput = False):
        data = self.tetramers.items()
        if data is None:
            raise Exception("Empty dictionary!")
        
        if sortOutput:
            data = self.CreateSortedTetramers()
        
        filename = outputPath
        with open(filename, 'w') as f:
            for key, tet in data:
                f.write("%s,%s\n"%(key, tet.freq))     

    def getRecords(self):
        return self.records
        
    def calculateExpectedProbability(self):
        if len(self.tetramers) == 0:
                raise Exception("Tetramer list empty! Run Count Tetramers")
        else:
            #for each tetramer, calculate its expected probability
            #by multiplying the probability value of its amino acids
            #with one another
     
            for tetramer in self.tetramers:
                expectedValue = 1.0
                #newKey = self.replace(tetramer)
                for aminoAcid in tetramer:
                    if aminoAcid == 'X':
                        aminoAcid = 'Q'
                    expectedValue = expectedValue * self.controlDict[aminoAcid]
                self.tetramers[tetramer].prob = expectedValue
                #print(expectedValue)

    #using control.csv a*b*c*d approach
    #this function sets our control values for each amino acid
    #from a formatted csv file.
    #Setting calcExpectedProb = False prevents the function from
    #calculating expected probability for every tetramer in our database
    def setControlFromFile(self, pathName, useAbsPath = False, calcExpectedProb = False):
        #creating a dictionary of amino acids that determine expected
        #probability for a given tetramer
        tetDict = {}
        #if we were given a relative path, instead of an absolute,
        # we convert it to an absolute path
        if useAbsPath is False:
            controlFileName = os.path.abspath(pathName)
        else:
            #if we were given an absolute path we just use it as is
            controlFileName = pathName 

        control= pd.read_csv(controlFileName)
        control=np.array(control)
        for aminoacid in control:
            tetDict[aminoacid[0] ] = aminoacid[1]
        
        self.controlDict = tetDict

        if calcExpectedProb is True:
            if len(self.tetramers) == 0:
                raise Exception("Tetramer list empty! Cannot compute expected probabilities.")
            else:
                #for each tetramer, calculate its expected probability
                #by multiplying the probability value of its amino acids
                #with one another
                for key in self.tetramers:
                    expectedValue = 1.0
                    for aminoAcid in key:
                        expectedValue = expectedValue * tetDict[aminoAcid]
                    self.tetramers[key].setProb(expectedValue)
            self.calculateExpectedProbability()


    #this also sets up the control file but uses a dictionary of amino acids
    #instead of a file. 
    def setControlFromDict(self, controlDict, calcExpectedProb = False):
        self.controlDict = controlDict
        if calcExpectedProb is True:
            if len(self.tetramers) == 0:
                raise Exception("Tetramer list empty! Cannot compute expected probabilities.")
            else:
                #for each tetramer, calculate its expected probability
                #by multiplying the probability value of its amino acids
                #with one another
                for key in self.tetramers:
                    expectedValue = 1.0
                    for aminoAcid in key:
                        expectedValue = expectedValue * tetDict[aminoAcid]
                    self.tetramers[key] = expectedValue
            self.calculateExpectedProbability()





    
