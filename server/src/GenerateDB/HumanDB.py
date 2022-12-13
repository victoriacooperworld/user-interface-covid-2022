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


'''
HumanDB is a script to do the checkings on different database(human, viral, bacteria, etc.)
For this function:
constructDB(): use this to construct a database.
check(): this is the function for pearson check part. Input params intro is inside the function
'''

RETURN_PATH = r"C:\Users\User\Desktop\user-interface-covid-2022\server\OutputFiles\DictFile.csv"

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
    db = databaseInit()
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


def check(inputPath, heap_size, pos_diff, selectedDB, outputPath):
    """
    inputs:
    inputpath: significant tetramer file's directory.
    heap_size: the size for the output proteins (could be 100,200,...)
    pos_diff: for the significant tetramer, how close they are. (in order to discover adjacent tetramers)
        eg. SSAL SALM (pos_diff = 1)
    selectedDB: the database that is going to be queried from
    """
    #input significant tetramers
    db = databaseInit()

    st = datetime.datetime.now()
    data = collections.defaultdict() # store the tetramer and it's p value in a dictionary
    with open(inputPath,'r') as f:
        while True:
            d= f.readline().strip('\n').split("\t")
            if len(d)!=2: break
            data[d[0]]=d[1]
    print(inputPath, heap_size, pos_diff, selectedDB)
    db.useDB(selectedDB)
    db.is_connected()
    proteinInfo = collections.defaultdict(Protein)
    for k,p in data.items(): #tetramers, p values
        #find significant proteins
        seq = "\'"+ k +"\'"
        entries = str(db.search("entries","tetramerid","sequence",seq)[0])
        if entries == r"('\r',)":
            print("Skipping ", k, p)
            print("Entries", entries)
            continue
        # print(entries)
        # entries=entries[3:-7]
        entry = entries.split("),(")
        
        entry[0]=entry[0][3:]  #fix the first element's form
        entry[-1] = entry[-1][:-7] #fix the last element's form

        for e in entry: #protein, pos
            try:
                a = e.split(',')
                proteinIdx = a[0]
                tetPos = a[1]
            except IndexError:
                print("HEYYY", a, proteinIdx, e, k, p)
                # break
                return
            if proteinInfo[proteinIdx].setSeen(k): continue
            else: 
                proteinInfo[proteinIdx].setSeen(k)
                proteinInfo[proteinIdx].setP(float(p))
                proteinInfo[proteinIdx].setPos((k,int(tetPos))) 
    print("start sorting...")
    heap = []
    #find the smallest
    for k,v in proteinInfo.items():
        heapq.heappush(heap,(-v.pValue,k,v.positions))
        if len(heap)>heap_size:
            heapq.heappop(heap)
    
    res_protein = []
    returnFilePath = outputPath

    for pair in heap:
        tmp=[]
        pos_diff_res=[]
        idx = pair[1]
        pValue = -pair[0]
        pos = pair[2] 
        a = sorted(pos,key = lambda  x:x[1]) # a is the tetramers in the protein
        a = [list(i) for i in a]
        print(a)
        des = db.search("description","proteinid","id",idx)[0]
        length = len(str(db.search("sequence","proteinid","id", idx)[0]))-7

        # generating the rows
        tmp.append(des) 
        tmp.append(pValue)
        tmp.append(length)
        tmp.append(pValue*length)
        tmp.append(str(a))
         
        
        #count postions
        for i in range(1,len(a)):
     
            if a[i][1]-a[i-1][1]<pos_diff:
                if a[i-1] not in pos_diff_res:
                    pos_diff_res.append(a[i-1])
                if a[i] not in pos_diff_res:
                    pos_diff_res.append(a[i])
        tmp.append(pos_diff_res)
        res_protein.append(tmp)

        # merge the tetramers to 1 if they are contiguous.
        i = 0
        while i < len(a)-1:
            if a[i+1][1]-a[i][1]<pos_diff:
                #implies a tetramer overlap
                if a[i+1][1] - a[i][1]<=len(a[0]):
                    diff = a[i+1][1] - a[i][1]
                    newSeq = a[i][0][:diff] + a[i+1][0]
                    newPair = [newSeq, a[i][1]]
                    a[i] =  newPair
                    del a[i+1]

                else:
                    i=i+1
            else:
                i = i+1

     
    
        # merged tetramers times p value as Dr. Glabe asked on 12/7/2022
        # get all the tetramers in the merged kmers - for example, SSSQ, SSQA -> SSSQA -> 2 tetramers
        # z value = the p value from the first tetramer 'SSSQ' divided by 20 ^ *(n-1), n is the number of tetramers in the merged tetramer

        for tetPair in a:
            firstTetramer = tetPair[0][:4]
            print(firstTetramer)
            if tetPair[0] == 4: continue
            firstTetPvalue = float(data[firstTetramer])
            zValue = firstTetPvalue/pow(20,len(firstTetramer)-4)

            print("zValue:"+ str(zValue))
            tetPair.append(zValue)

        tmp.append(a)

    file=open(returnFilePath,"w")
    df = pd.DataFrame(res_protein)
    head = ["Description", "P Value", "Length of the Protein", "P Value * Length", "Tetramers, Postion", "Tetramers Filtered by Position Difference by " + str(pos_diff), "Merged Tetramer, Position, ZValue"]
    df.to_csv(file, mode="a", header=head, index = False, line_terminator="\n")


    # file.close()

    et = datetime.datetime.now()

    print("Time used:" + str(et-st))

    return returnFilePath


# inputPath = r"C:\Users\User\Desktop\Alzheimers\Top20.txt"
# heap_size  = 100
# pos_diff =  20
# selectedDB = 'humandb'

# check(inputPath, heap_size, pos_diff, selectedDB)


if __name__ == '__main__':
    ret1 = check(r'C:\Users\User\Desktop\BrucellaData\Top20_Brucella_SigTetramers.txt',25,100,'bacteriadb')
    print(ret1)