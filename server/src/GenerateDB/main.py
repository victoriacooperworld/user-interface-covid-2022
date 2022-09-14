#!/usr/bin/env pyp
import collections
import csv
import datetime
import multiprocessing
from multiprocessing.dummy import Process
import os
from re import T
import shutil
import sys
import logging
from time import sleep
from turtle import position
import mysql.connector
from numpy import isin
import STetramerNRlarge as STetramerNRlarge
import DatabaseInit as DatabaseInit


# from Bio import SeqIO

base_address = os.path.dirname(sys.path[0])
f88 = f"{base_address}\\InputFiles\\NR_Data\\f88.fna"
f1k = f"{base_address}\\InputFiles\\NR_Data\\f1k.fna"
first10000 = f"{base_address}\\InputFiles\\NR_Data\\First10000proteins_of_nr.fna"
first200000 = f"{base_address}\\InputFiles\\NR_Data\\First200000proteins_of_nr.fna"
f100k = f"{base_address}\\InputFiles\\NR_Data\\100k.fna"
f2m = f"{base_address}\\InputFiles\\NR_Data\\f2m.fna"
f1m = f"{base_address}\\InputFiles\\NR_Data\\f1m.fna"
theBigBoy = r"E:\Non-redundantProteome\nr\nr"
f500k =f"{base_address}\\InputFiles\\NR_Data\\f500k.fna"




def consumer_compute(work1,work2):

    totNum = 0
    while (True):  
        curEntry  = work1.get()
        if curEntry == -1:
            work2.put(curEntry)
            
            return 

        idNum = curEntry[0]
        header = curEntry[1]
        curSequence = curEntry[2]

        # sequenceData = str(curSequence._seq)
        sequenceData = curSequence.replace("X","Q")
        sequenceData = sequenceData.replace("J","L")
        sequenceData = sequenceData.replace("Z","Q")
        sequenceData = sequenceData.replace("U","A")
        sequenceData = sequenceData.replace("B","N")

        descript = header[1:-1]
        exportDict = collections.defaultdict(str)
        data = [str(idNum), descript, sequenceData]
        work2.put(data, block = True)
        proteinIdStr = str(idNum)

        for i in range(0,len(sequenceData) - 4):
            curTetramer = str(sequenceData[i:i+4])
            curProtPos = '(' + proteinIdStr + ',' + str(i) + '),'
            exportDict[curTetramer] += curProtPos
        # print(proteinIdStr)

        
        work2.put(exportDict, block = True)

        totNum +=1


def consumer_write(tetTableName, proteinTableName,work2):
    db = DatabaseInit.databaseInit()
    db.useDB("ProteinDB")
    while True:
        print(work2.qsize())
        data  = work2.get()

        if data == -1:
            print('Reached to the end')
            print(datetime.datetime.now())
            return
            
        if isinstance(data, list):
            # TODO: insert into proteinid
            # print("Insert into protein table")
            db.insertDataOneProtein(data,  proteinTableName, columnNames = "(Id, Description, sequence)")

        else:
            # TODO: insert into tetramerid
            for tet, positionData in data.items():
                try:
                    # print("Insert into tetramer table")
                    db.concat(tetTableName, "Entries", positionData, "Sequence", tet)
                    
                except IndexError:
                    print("Export entry", tet, positionData)
                    quit()


def consumer_write_txt(work2, fixedDict, filename,numComputers, outputDir, chunkSize = 1000000):
    # create 2 txt files
    basename = os.path.basename(filename)
    print("Basename is ", basename)
    p = os.path.join(outputDir, "ProteinID")
    p = os.path.join(p,  basename.split('.')[0] + '.txt')
    t = os.path.join(outputDir, "TetramerID")
    t = os.path.join(t,  basename.split('.')[0] + '.txt')
    protId = open(p,"w")


    # p = f'C:\\Users\\User\\Desktop\\covidProject-2022Summer\\OutputFiles\\ProteinID\\' + basename.split('.')[0] + '.txt'
    # t = f'C:\\Users\\User\\Desktop\\covidProject-2022Summer\\OutputFiles\\TetramerID\\' + basename.split('.')[0] + '.txt'
    # protId = open(f'C:\\Users\\User\\Desktop\\covidProject-2022Summer\\OutputFiles\\ProteinID\\' + basename.split('.')[0] + '.txt',"w")

   
    tetId = t
    tetDict = fixedDict
    numProts = 0
    computeFinished = 0

    while (True): 
        if numProts == chunkSize:
            OutputToTxt(tetId, tetDict)
            tetDict.clear()
            tetDict = fixedDict
            numProts = 0

        data = work2.get()
            
        if data == -1:
            computeFinished +=1
            if computeFinished == numComputers:
                OutputToTxt(tetId, tetDict)   
                break
            continue


        if isinstance(data, list):
            # TODO: insert into proteinid
            # print("Insert into protein table")

            protId.write('|'.join(data))

            
        

        else:
            # TODO: insert into tetramerid
            for tet, positionData in data.items():
                tetDict[tet] += positionData
        numProts+=1
    protId.close()
    print('Reached to the end')
    return

def OutputToTxt(outputPath,tetDict):
    print(outputPath)
    f = open(outputPath, 'w')
    for tet, data in tetDict.items():
        f.write(data +'\n')
        f.flush()
    
    f.close()

def mergeTxt(path1, path2, path3, deletePath1 = False, deletePath2 = False):
    st = datetime.datetime.now()
    f1 = open(path1, 'r')
    f2 = open(path2, 'r')
    f3 = open(path3, 'w')

    # f1lines = f1.readlines()
    # f2lines = f2.readlines()


    # for line1, line2 in zip(f1lines, f2lines):
    #     f3.write("{}{}\n".format(line1.rstrip(),line2.rstrip()))
    for i in range(0,160000):
        line1 = f1.readline().strip("\n")
        line2 = f2.readline()
        
        line3 = line1+line2

        f3.write(line3)

    f1.close()
    f2.close()
    f3.close()

    if deletePath1:
        os.remove(path1)
    if deletePath2:
        os.remove(path2)

    et = datetime.datetime.now()
    timetotal = et-st
    print("Time taken for merge was ", timetotal)

def mergeTxt_mp(curDirectory, deleteOriginals = False):
    while(True):
        path1 = curDirectory.get()
        if(path1 == -1):
            return
        path2 = curDirectory.get()
        if(path2 == -1):
            if path1 != -1:
                print(path1, " Was not merged into anything.")
            return
        # print("Path 1:", path1)
        # print("Path 2:", path2)
        path3 = os.path.join(os.path.dirname(path1),"Merged") 
        path3 = os.path.join(path3,os.path.basename(path1))
        # print(path3)
        st = datetime.datetime.now()
        f1 = open(path1, 'r')
        f2 = open(path2, 'r')
        f3 = open(path3, 'w')

        # f1lines = f1.readlines()
        # f2lines = f2.readlines()


        # for line1, line2 in zip(f1lines, f2lines):
        #     f3.write("{}{}\n".format(line1.rstrip(),line2.rstrip()))

        for i in range(0,160000):
            line1 = f1.readline().strip("\n")
            line2 = f2.readline()
            
            line3 = line1+line2

            f3.write(line3)


        f1.close()
        f2.close()
        f3.close()
        et = datetime.datetime.now()
        timetotal = et-st
        print("Time taken for merge was ", timetotal)
        if deleteOriginals:
            os.remove(path1)
            os.remove(path2)


def Process_MergeTxt(dirPath, deleteOriginals = False):
    #until we have all files merged, do loop

    manager = multiprocessing.Manager()
    curDirectory = manager.Queue()
    pool = []
    num_merger = 1
    #initialize work queue
    dir =  os.listdir(dirPath) 
    for filee in dir:
        #skip directories
        if os.path.isdir(os.path.join(dirPath,filee)):
            continue
        curDirectory.put(os.path.join(dirPath,filee))
    #create processes
    for i in range(0,num_merger):
        writing_process = multiprocessing.Process(target=mergeTxt_mp, args=(curDirectory,deleteOriginals))
        pool.append(writing_process)
        writing_process.start()
    #create kill orders

    for process in range(0,num_merger):
        curDirectory.put(-1)
    #rejoin processes before beginning next cycle
    for process in pool:
        if process.is_alive():
            print("joining...")
            process.join()


def Process_MergeTxt_Auto(dirPath):
    directory = os.listdir(dirPath)
    if len(directory) == 1:
        return
    os.mkdir(os.path.join(dirPath,"Merged"))
    if len(directory) %2 != 0:
        lastFile = directory[-1] 

        shutil.move(os.path.join(dirPath, lastFile),  os.path.join(os.path.join(dirPath,"Merged"), lastFile) )
    directory = directory[:-1]
    for i in range(0, len(directory), 2):
        curPath1 = os.path.join(dirPath,directory[i])
        curPath2 = os.path.join(dirPath,directory[i+1])
        mergeTxt(curPath1, curPath2, os.path.join(os.path.join(dirPath,"Merged"),directory[i]) , deleteOriginals = True)
    
    Process_MergeTxt_Auto(os.path.join(dirPath,"Merged"))



def MakeKeyColumn(path, tetDict):
    f = open(path, 'w')
    for key in tetDict.keys():
        f.write(key + "|" +'\n')
    f.close()





def process(file, res,  outputDir):

    manager = multiprocessing.Manager()
    work1 = manager.Queue()
    work2 = manager.Queue()
    numCores = multiprocessing.cpu_count()

    num_compute = 22
    num_writer = 1
    
    pool = []
    logging.critical("Spawning processes")


    #create other computing process
    for i in range(0,num_writer):
        writing_process = multiprocessing.Process(target=consumer_write_txt, args=(work2,res,file, num_compute, outputDir))
        pool.append(writing_process)
        writing_process.start()


    for i in range(0,num_compute):
        p = multiprocessing.Process(target=consumer_compute, args=(work1,work2,))
        p.start()
        pool.append(p)
 

    fileNum = os.path.basename(file)
    fileNum = fileNum.strip("File")
    fileNum = fileNum.strip(".fna")
    fileNum = int(fileNum.strip(".txt"))
    idNum = fileNum * 100000
    
    try:
        st = datetime.datetime.now()
        print(st)
        
        with open(file) as f:
            
            while (True):
                header = f.readline()
                seq = f.readline()
                if not seq:
                    break         
                entry = [idNum, header, seq]
                work1.put(entry, block=True)
                idNum +=1

    except StopIteration:
        pass
    print("Read in ", str(i), " lines")
    # logging.critical("100 percent complete")
    for process in pool:
        work1.put(-1)
    
    # Joining back together
    for process in pool:
        if process.is_alive():
            print("joining...")
            process.join()
 
    
    work1._close()
    # work2._close()
   
    et = datetime.datetime.now()
    timetotal = et-st
    print("Time taken was ", timetotal)
    return idNum



if __name__ == '__main__':
    

    # print("Operating on ", numCores, " cores")  
    db = DatabaseInit.databaseInit()
    # db.createTable('ProteinID',"(Id int , Description mediumtext,Sequence longTEXT ,PRIMARY KEY (Id) )") 
    # db.create_index("proteinid", "Id")

    # db.createTable('TetramerID',"(Sequence VARCHAR(4), Probability VARCHAR(15), Entries longTEXT)")
    # db.create_index("tetramerid", "Sequence")

    path = f"{base_address}\..\InputFiles\Control.csv"
    controlDict = STetramerNRlarge.readFile(path)
    res = STetramerNRlarge.generateTetramerStr(controlDict)

    # dir = r"C:\Users\User\Desktop\covidProject-2022Summer\InputFiles\Test"
    
    # ------------------------------------------------------# 
    dir = r"V:\Human\Human" 
    outputDir = r"V:\Human"
    SortedFiles = os.listdir(dir)
    SortedFiles.sort()
    for file in SortedFiles:
        print("Start process " + file)
        st = datetime.datetime.now()
        process(os.path.join(dir,file), res, outputDir)
        et = datetime.datetime.now()
        print("Time used for " + file + " is " + str(et-st))
    # process(os.path.join(dir,file),res,outputDir)
    # ------------------------------------------------------#

    # dir = r"D:\OutputFiles1\TetramerID\Merged"
    # st = datetime.datetime.now()
    # #Process_MergeTxt(dir, deleteOriginals=False)
    # Process_MergeTxt(dir)
    # et = datetime.datetime.now()
    # timetotal = et-st
    # print("Total time taken was ", timetotal)






   
   

