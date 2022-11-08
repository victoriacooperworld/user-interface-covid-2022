
#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 07:58:22 2021

@author: Keane Wong
"""

import collections
from enum import unique
import itertools
import os,sys, time
from re import I
import logging
from urllib.request import AbstractDigestAuthHandler
import pandas as pd
from Bio import SeqIO
import numpy as np
from Bio.SeqIO.FastaIO import SimpleFastaParser
import DatabaseInit 
from multiprocessing import pool, cpu_count

import datetime




def createTotalDB_MP(importQueue, chunkSize = 1000):
    protCounter = 0
    while (True):   
        curEntry  = importQueue.get()
        if curEntry is None:
            return 
        idNum = curEntry[0]
        header = curEntry[1]
        curSequence = curEntry[2]
         
        # sequenceData = str(curSequence._seq)
        sequenceData = curSequence.replace("X","Q")
        descript = ' '.join(header.split(' ')[1:-1])
        exportDict = collections.defaultdict(str)
        data = [idNum, descript, sequenceData]
    
        # db.insertDataOneProtein(data,  proteinTableName, columnNames = "(Id, Description, sequence)")
    
        proteinIdStr = str(idNum)
        

        for i in range(0,len(sequenceData) - 3):
            curTetramer = str(sequenceData[i:i+4])
            curProtPos = '(' + proteinIdStr + ',' + str(i) + '),'
            exportDict[curTetramer] += curProtPos
        # db.useDB("ProteinDB")

        if protCounter % chunkSize == 0:
            for tetramer, protData in exportDict:
                db.concat("TetramerId", "entries", protData, "Tetramer", tetramer)
                exportDict = collections.defaultdict(str)

def readFile(path):
    controlDict = {}
    control = pd.read_csv(path)
    control = np.array(control)
    for entry in control:
        controlDict[entry[0]] = entry[1]
    return controlDict


def countProbability(tetramerString, controlDict):
    res = 1.0
    for aminoAcid in tetramerString:
        res = res * controlDict[aminoAcid]

    return res

def generateTetramer(controlDict: dict):
    Control = list(controlDict.items())
    res = collections.defaultdict(float)
    #nested loop that outputs every permutation of a 4 part sum, with column 0 in aa and column 1 in ff
    #this creates an array of all possible 4 sequence chains and the probabilities of each 4 sequence
    #total of 20^4 combinations
    for i in range(len(Control)):
        for j in range(len(Control)):
            for k in range(len(Control)):
                for l in range(len(Control)):
                    aa=Control[i][0]+Control[j][0]+Control[k][0]+Control[l][0]
                    ff=Control[i][1]*Control[j][1]*Control[k][1]*Control[l][1]
                    #aac is a given tetramer combination and ffc is the expected probability it happens
                    res[aa] = ff
    return res
                    
def generateTetramerStr(controlDict: dict):
    Control = list(controlDict.items())
    res = collections.defaultdict(str)
    #nested loop that outputs every permutation of a 4 part sum, with column 0 in aa and column 1 in ff
    #this creates an array of all possible 4 sequence chains and the probabilities of each 4 sequence
    #total of 20^4 combinations
    for i in range(len(Control)):
        for j in range(len(Control)):
            for k in range(len(Control)):
                for l in range(len(Control)):
                    aa=Control[i][0]+Control[j][0]+Control[k][0]+Control[l][0]
         
                    res[aa] = ""
    return res

#controlFileName is the file where you read in protein sequences
#DirName is the directory containing the information
#if isDefault is true, we use the default list of amino acids
def CreateIDList(DirName, db, proteinTableName, sendToCSV = False, outputPath = None):
    if sendToCSV:
        if not outputPath:
            print("Error: output path not specified for csv file")
            quit()
    logging.critical("Starting function 'CreateIDList' in STetramerNR.py")
    
    unique_ID = []
    descriptor = []
    lengths = []
    correspond_id = []
    idIter = 0
    path = DirName  
    ###read all data in this folder: NR_Data
    all_files = os.listdir(path)

    records_list = []
    percentage = 0
    linesProcessed = 0
    st = datetime.datetime.now()
    for fle in all_files:    
        SequenceFile = os.path.join(path,fle)
        print(SequenceFile)

        record_iterator = SeqIO.parse(SequenceFile,"fasta")
        try:
            while (True):
                linesProcessed = linesProcessed+1
                if (linesProcessed % 4161000) == 0 and linesProcessed != 0:
                    percentage = percentage+1
                    logging.critical("%s percent of ID list done", percentage)
                curSequence = next(record_iterator)


                descript = curSequence.description


                seqData = str(curSequence._seq)
                data = [descript, seqData]
              

                db.insertDataOneProtein(data,  proteinTableName, columnNames = "(Description, sequence)")
                
                
                if sendToCSV:
                    print(curSequence)
                    #correspond_id.append(hex(idIter))
                    #unique_ID.append(pid)
                    descriptor.append(descript)
                    #lengths.append(lengthSeq)
                #idIter = idIter +1 
        except StopIteration:
            pass
        logging.critical("Completed ID List")



        #code used to output to csv
        if sendToCSV:
            logging.critical("Exporting to dataframe")
            unique_ID_List = pd.DataFrame({'ID':correspond_id, 'Sequence':unique_ID, 'Description': descriptor, 'Length': lengths})
            logging.critical("Exporting to csv")
            unique_ID_List.to_csv(outputPath)
            print(unique_ID_List)
        et = datetime.datetime.now()
        timetotal = et-st
        print("Time taken was ", timetotal)


def createTetramerTable( DirName,tetTableName):
    idIter = 0
    linesProcessed = 0
    percentage = 0
    path = DirName

    all_files = os.listdir(path)

    db = DatabaseInit.databaseInit()
    if db.is_connected():
        print("DB is connected!")

    st = datetime.datetime.now()
    for fle in all_files:
        SequenceFile = os.path.join(path,fle)
        record_iterator = SeqIO.parse(SequenceFile,"fasta")
        try:
            
            while (1):
                linesProcessed = linesProcessed+1
                if (linesProcessed % 4161000) == 0 and linesProcessed != 0:
                    percentage = percentage+1
                    logging.critical("%s percent of ID list done", percentage)
                curSequence = next(record_iterator)
                sequenceData = str(curSequence._seq)
                proteinID = hex(idIter)
                idIter = idIter+1
                exportDict = {}
                
                for i in range(0,len(sequenceData) - 3):
                    curTetramer = str(sequenceData[i:i+4])
                    curTetramer = curTetramer.replace("X","Q")
                    curProtPos = '(' + str(proteinID) + ',' + str(i) + '),'
                    #exportEntry = [curTetramer, curProtPos]
                    exportDict[curTetramer] = curProtPos

                db.useDB("ProteinDB")
                for tet, positionData in exportDict.items():
                    
                    try:
                        db.concat(tetTableName, "Entries", positionData, "Sequence", tet)
                        
                    except IndexError:
                       
                        print("Export entry", tet, positionData)
                        quit()
                del curSequence
                del exportDict
        except StopIteration:
            pass
    et = datetime.datetime.now()
    timetotal = et-st
    print("Time taken was ", timetotal)
    print("Finished creatintg db")
            
def CreateTotalDB(DirName,db,tetTableName, proteinTableName):
    linesProcessed = 0
    percentage = 0
    path = DirName
    proteinId = 0
    all_files = os.listdir(path)

    st = datetime.datetime.now()
    for fle in all_files:
        SequenceFile = os.path.join(path,fle)
        record_iterator = SeqIO.parse(SequenceFile,"fasta")
        try:
            
            while (1):
                linesProcessed = linesProcessed+1
                if (linesProcessed % 4161000) == 0 and linesProcessed != 0:
                    percentage = percentage+1
                    logging.critical("%s percent of ID list done", percentage)
                curSequence = next(record_iterator)
                sequenceData = str(curSequence._seq)
                descript = curSequence.description
                #proteinID = hex(idIter)
                
                exportDict = collections.defaultdict(str)
                
                data = [descript, sequenceData]
              

                db.insertDataOneProtein(data,  proteinTableName, columnNames = "(Description, sequence)")
                
                proteinIdStr = str(proteinId)
                for i in range(0,len(sequenceData) - 3):
                    curTetramer = str(sequenceData[i:i+4])
                    #curTetramer = curTetramer.replace("X","Q")
                    curProtPos = '(' + proteinIdStr + ',' + str(i) + '),'
                    #exportEntry = [curTetramer, curProtPos]
                    exportDict[curTetramer] += curProtPos

                db.useDB("ProteinDB")
                for tet, positionData in exportDict.items():
                    #concat(self, tableName, updateColumn, strConcat, columnName, targetValue)
                    try:
                        tett = tet.replace("X", "Q")
                        db.concat(tetTableName, "Entries", positionData, "Sequence", tett)
                        
                    except IndexError:
                       
                        print("Export entry", tet, positionData)
                        quit()
                proteinId+=1

        except StopIteration:
            pass
    et = datetime.datetime.now()
    timetotal = et-st
    print("Time taken was ", timetotal)
    print("Finished creatintg db")





