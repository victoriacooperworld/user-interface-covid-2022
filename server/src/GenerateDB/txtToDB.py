
import csv
from datetime import datetime
from DatabaseInit import databaseInit
import csv
from tokenize import String
# import pandas as pd
import mysql.connector 
import os
from mysql.connector import Error

def TextToCsv(inputDir, outputDir):
    for file in os.listdir(inputDir):
        filepath = os.path.join(inputDir,file)
        outfilename = file.replace(".txt",".csv")
        outFilepath = os.path.join(outputDir,outfilename)
        with open(filepath, 'r') as f:
            with open(outFilepath,'w') as fo:
                while True:
                    line = f.readline()
                    if not line:
                        f.close()
                        fo.close()
                        break
                    lineParts = line.split('|')
                    lineParts[1] = '"' + lineParts[1] + '"'
                    fo.write(",".join(lineParts))

            

if __name__ == '__main__':
    # # This script is to put the data in merge.txt to database
    # db = databaseInit()

    # path = r'D:\OutputFiles\ProteinID\1.txt'
 
    
    # # db.createTable('ProteinID_NR',"(Id int , Description mediumtext, Sequence longTEXT)") 
    # # db.create_index("proteinid", "Id")
    # st = datetime.now()
    # # f = csv.reader(open(path))
    # # header = next(f)
    # db.useDB("proteindb")
    # line = 0
    # with open(path,"w") as f:
    #     print("start.....")
    #     row = f.readline()
       
    #     tet = row[0]
    #     positionData = row[1]
    #     db.concat("tetramerid", "Entries", positionData, "Sequence", tet)
    #     line+=1
    #     # the connection is not autocommitted by default, so we must commit to save our changes

  
    # et = datetime.now()
    # print("time used: ", et-st)
    TextToCsv(r'D:\OutputFiles\ProteinID',r'D:\OutputFiles\ProteinID_csv')

    