import collections
import csv
import os
import pandas as pd
from GenerateDB.DatabaseInit import databaseInit
from Patient import PatientProtein
from PatientInput import Input
import GenerateDB.STetramerNRlarge as st
import scipy
import matplotlib.pyplot as plt

import numpy as np
def pcc(X, Y):
   ''' Compute Pearson Correlation Coefficient. '''
   # Normalise X and Y
   X -= X.mean(0)
   Y -= Y.mean(0)
   # Standardise X and Y
   X /= X.std(0)
   Y /= Y.std(0)
   # Compute mean product
   return np.mean(X*Y)



def readStandard():
    file = r"C:\Users\User\Desktop\Alzheimers\Pos.txt"
    total = 0
    significantSeq = set()
    cnt=collections.defaultdict(float)
    with open(file,'r') as f:
        while True:
            d= f.readline().strip('\n').split("\t")
            if len(d)!=2: break
            significantSeq.add(d[0])
            cnt[d[0]]+=float(d[1])
    return cnt,total,significantSeq

def toList(controlCnt, cnt):
    list1 = []
    for c in controlCnt:
        list1.append(cnt[c])
    return list1

def constructNewDict(control):
    newDict = collections.defaultdict()
    for c in control:
        newDict[c]=0
    return newDict

cnt,total,control = readStandard()

def wholeDir(path):
    totalTetramer=collections.defaultdict(list)

    def readPatient(path, fileName, control, newDict):
        sequences, totalTet= Input.readOneFNAFile(path, fileName)
        for record in sequences:
            protein, count = record[0], int(record[1])
            # print(protein, count)
            for i in range(len(protein)-3):
                tetramer = protein[i:i+4]
                if tetramer not in control: continue
                newDict[tetramer]+=count

        ret = collections.defaultdict(float)
        for c in newDict:   
            ret[c] = newDict[c]/totalTet
        return ret
   
    # print(totalTetramer)
    for file in os.listdir(path):
        newDict = constructNewDict(control)
        cnt=readPatient(path, file, control, newDict)
  
        for c in cnt:
            totalTetramer[c].append(cnt[c])
    return totalTetramer

def isSameProtein(tet1, tet2, dbName, tableName):
    """
    Give 2 tetramers and see the proteins they are both in 
    """
    db = databaseInit()
    db.useDB(dbName)
    listSameProt = []
    tet1 = "\'"+ tet1 +"\'"
    entries = str(db.search("entries","Tetramerid","sequence",tet1)[0])
    entry = entries.split("),(")
    entry[0]=entry[0][3:]  #fix the first element's form
    entry[-1] = entry[-1][:-7] #fix the last element's form
    entryDict1 = collections.defaultdict(int)
    for ent in entry:
        d = ent.split(',')
        entryDict1[d[0]] = int(d[1])

    tet2 = "\'"+ tet2 +"\'"
    entries2 = str(db.search("entries","Tetramerid","sequence",tet2)[0])
    entry2 = entries2.split("),(")
    entry2[0]=entry2[0][3:]  #fix the first element's form
    entry2[-1] = entry2[-1][:-7] #fix the last element's form
    entryDict2 = collections.defaultdict(int)
    for ent in entry2:
        d = ent.split(',')
        entryDict2[d[0]] = int(d[1])
    
    desList = []
    eProt1 = []
    eProt2 = []
    for prot in entryDict1.keys():
        if prot in entryDict2.keys():
            des = str(db.search("description","Proteinid","id",prot)[0])
            des+=" "+ str(entryDict1[prot])+" , "+ str(entryDict2[prot])
            desList.append(des)
            eProt1.append(entryDict1[prot])
            eProt2.append(entryDict2[prot])
    listSameProt.append(desList)
    # listSameProt.append(eProt1)
    # listSameProt.append(eProt2)
    return listSameProt

        


tet=wholeDir(r'C:\Users\User\Desktop\Alzheimers\AD')
dir = r'C:\Users\User\Desktop\Alzheimers\sameProtein'
res=[]
#compare 2 tetramers
significantTet=list(control)
print(significantTet)
for i in range(len(significantTet)-1):
    for j in range(i+1,len(significantTet)):
        tmp=[]
        l1=tet[significantTet[i]]
        l2 = tet[significantTet[j]]
        r, p = scipy.stats.pearsonr(l1,l2)
        tmp.append(significantTet[i])
        tmp.append(significantTet[j])
        tmp.append(r)
        tmp.append(p)
        ee = isSameProtein(significantTet[i],significantTet[j],"Humandb", 'tetramerid')
 
        if len(ee[0])!=0 and r>0.5:
            list1=[significantTet[i],significantTet[j]]+[str(r)]+[str(p)]
            list2 = list1+ee[0]
            fileName = significantTet[i]+","+significantTet[j]+".csv"
            file=open(os.path.join(dir,fileName),"w")
            df = pd.DataFrame(list2)
            df.to_csv(file, mode="a", header=False, index = False, line_terminator="\n")
            file.close()
            
        tmp+=ee
        res.append(tmp)



# file=open(r'C:\Users\User\Desktop\pearson.csv',"w")
# df = pd.DataFrame(res)
# head = ["Tetramer1","Tetramer2","P Value", "R Value", "Belonged Protein", "Tetramer1 Position","Tetramer2 Position"]
# df.to_csv(file, mode="a", header=False, index = False, line_terminator="\n")

# file.close()

