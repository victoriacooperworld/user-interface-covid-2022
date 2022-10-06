#create the human db

import collections
import csv
import datetime
import heapq
from html import entities
import math
import os
import sys
# from turtle import position

import sys
sys.path.append('src/GenerateDB')
from DatabaseInit import databaseInit
# import STetramerNRlarge
# import DatabaseInit
import pandas as pd



class Protein:
    def __init__(self) -> None:
        self.seen = set()
        self.length = 0
        self.positions=[]
        self.pValue=1
        self.des = ''
    def setSeen(self, tetramer):
        if tetramer in self.seen:
            return True
        else:
            self.seen.add(tetramer)
            return False

    def setPos(self, pair):
        self.positions.append(pair)

    def setP(self, p):
        self.pValue = self.pValue*p

    def setDes(self, des):
        self.des = des
    
    def setLength(self, length):
        self.length = length

def constructDB():
    base_address = os.path.dirname(sys.path[0])
    db = DatabaseInit.databaseInit()
    # db.useDB("HumanDB")
    db.createDB("HumanDB")

    db.createTable('ProteinID',"(Id int , Description mediumtext,Sequence longTEXT ,PRIMARY KEY (Id) )") 
    db.create_index("proteinid", "Id")

    db.createTable('TetramerID',"(Sequence VARCHAR(4), Probability VARCHAR(15), Entries longTEXT)")
    db.create_index("tetramerid", "Sequence")

    path = f"{base_address}\..\InputFiles\Control.csv"
    controlDict = STetramerNRlarge.readFile(path)
    res = STetramerNRlarge.generateTetramerStr(controlDict)

    # dir = r'D:\Human Files\Human\Human'
    # outputDir = r"V:\Human"
    # main.process(dir,res,outputDir)
    # # uncomment to fix the delimiter
    # dirPath = r'V:\Human\ProteinID'
    # outdir =  r'V:\Human\ProteinIDFixed'
    # DatabaseInit.FixDelimiters(dirPath, outdir)
        
    # pathControl = f"{base_address}\..\InputFiles\Control.csv"
    # controlDict = STetramerNRlarge.readFile(pathControl)
    # res = STetramerNRlarge.generateTetramer(controlDict)
    # keyPath = r'V:\Human\ProteinIDFixed\Key.txt'
    # main.MakeKeyColumn(keyPath, res)

    tetramersDir = r'V:\Human\TetramerID'
    outputTetramersDir = r'V:\Human\WithKeys'

    #Merged tetramer id files with a key 
    # for file in os.listdir(tetramersDir):
    #     st = datetime.datetime.now()
    #     pathName = os.path.join(tetramersDir, file)
    #     outputPath = os.path.join(outputTetramersDir,file)
    #     print(pathName, outputPath)
    #     main.mergeTxt( keyPath, pathName,outputPath, deletePath2 = True)
    #     et=datetime.datetime.now()
    #     print("Time used: "+str(et-st))

    insertProteins()


def check(inputPath, heap_size, pos_diff):
    #input significant tetramers
    db = databaseInit()
    db.useDB("HumanDB")

    st = datetime.datetime.now()
    data = collections.defaultdict()
    with open(inputPath,'r') as f:
        while True:
            d= f.readline().strip('\n').split("\t")
            if len(d)!=2: break
            data[d[0]]=d[1]

    db.useDB("HumanDB")
    proteinInfo = collections.defaultdict(Protein)
    for k,p in data.items(): #tetramers, p values
        #find significant proteins
        seq = "\'"+ k +"\'"
        entries = str(db.search("entries","Tetramerid","sequence",seq)[0])
        # print(entries)
        # entries=entries[3:-7]
        entry = entries.split("),(")
        
        entry[0]=entry[0][3:]  #fix the first element's form
        entry[-1] = entry[-1][:-7] #fix the last element's form

        for e in entry: #protein, pos
            a = e.split(',')
            proteinIdx = a[0]
            tetPos = a[1]
            if proteinInfo[proteinIdx].setSeen(k): continue
            else: 
                proteinInfo[proteinIdx].setSeen(k)
                proteinInfo[proteinIdx].setP(float(p))
                proteinInfo[proteinIdx].setPos((k,int(tetPos))) 
               

    print("start sorting...")
    result = []
    heap = []


    #find the smallest
    for k,v in proteinInfo.items():
        heapq.heappush(heap,(-v.pValue,k,v.positions))
        if len(heap)>heap_size:
            heapq.heappop(heap)
    
    res_protein = []
    returnFilePath = r"C:\Users\User\Desktop\user-interface-covid-2022\server\OutputFiles\DictFile.csv"
    file = open("OutputFiles\DictFile.txt","w")   
    for pair in heap:
        
        tmp=[]
        pos_diff_res=[]
        idx = pair[1]
        pValue = -pair[0]
        pos = pair[2] 
        a = sorted(pos,key = lambda  x:x[1])
        des = db.search("description","Proteinid","id",idx)[0]
        length = len(str(db.search("sequence","Proteinid","id", idx)[0]))-7
        tmp.append(pValue)
        tmp.append(length)
        tmp.append(pValue*length)
        tmp.append(str(a))
        tmp.append(des)  
        
        #count postions
        for i in range(1,len(a)):
            print(a[i][1],  a[i-1][1])
            if a[i][1]-a[i-1][1]<pos_diff:
                if a[i-1] not in pos_diff_res:
                    pos_diff_res.append(a[i-1])
                if a[i] not in pos_diff_res:
                    pos_diff_res.append(a[i])
        tmp.append(pos_diff_res)
        res_protein.append(tmp)

    print(res_protein)

    df = pd.DataFrame(res_protein)
    df.to_csv(returnFilePath)

    file.close()

    et = datetime.datetime.now()

    print("Time used:" + str(et-st))

    return returnFilePath