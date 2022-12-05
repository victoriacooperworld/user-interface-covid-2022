import collections
import math
import pandas as pd
import mysql.connector 
from mysql.connector import Error
from GenerateDB.DatabaseInit import databaseInit
from Patient import TetramerInfo
import matplotlib.pyplot as plt

"""
This is a script for plotting, but in the later version of the program we don't use it anymore.
"""
class tPlotInfo():
    def __init__(self, info: TetramerInfo, pos: int) -> None:
        self.info = info
        self.position = pos

class pPlotInfo():
    def __init__(self) -> None:
        self.tetramerList = [] #a list of tPlotInfo
        self.pValue = None
class Plotting:
    mydb = databaseInit()
    plotProtein  = collections.defaultdict(pPlotInfo) #key:protein name, value: pValues
    index = []
    
    def processInput(self, tetramerList: list(TetramerInfo),pType):
         for t in tetramerList:
            #find the tetramer in the database
            
            p = tPlotInfo(t,-1) #initialize the position to -1
            tname= t.sequence
            if pType == 'Bonferroni': 
                tp = t.Bonferroni
            elif pType == 'BH':
                tp = t.BH
            else:
                raise Exception("Invalid type! Try Bonferroni or BH")

            entries = self.mydb.search("TetramerID", tname, 'ENTRIES')
            entries = entries[1:-1] #get rid of the first and the last '[]'
            entry = entries.split(',')
            for e in entry: #iterate all the proteins
                info =  e[1:-1].split(",")
                idx,p.position = info[0], info[1] #this tetramer's pos in this protein
                #select id from proteinID where sequence == idx
                #return the protein name from protienID table from DB
                proteinName = self.mydb.search('id', 'proteinID', 'sequence', idx)  
                if not self.plotProtein[proteinName]:
                    proteinInfo = pPlotInfo()
                    proteinInfo.tetramerList.append(p)
                    proteinInfo.pValue *= tp
                    self.plotProtein[proteinName] = proteinInfo
                else:
                    self.plotProtein[proteinName].tetramerList.append(p)
                    self.plotProtein[proteinName].pValue *= tp

    def drawPlot(self):
        x=self.plotProtein.keys()
        y =[]
        for i in self.plotProtein.values():
            y.append(-math.log(i.pValue))
        plt.xlabel("Proteins")
        plt.ylabel("-log(p)")
        plt.scatter(x, y, c ="blue")
        plt.show()    
 
    def drawPlotMagnifier(self, proteinName,pType):
        """
        For each protein
        use tetramers' position as x-axis and its pValue as y-axis
        """
        t = self.plotProtein[proteinName].tetramerList #get all the related tetramers' info
        x,y= [],[]
        for i in t:
            x.append(i.pos)

            if pType == 'Bonferroni': 
                y.append(-math.log(i.info.pBonferroni))
            elif pType == 'BH':
                y.append(-math.log(i.info.pBH))
            else:
                raise Exception("Invalid type! Try Bonferroni or BH")
        
        plt.xlabel("Positions")
        plt.ylabel("-log(p)")
        plt.scatter(x, y, c ="blue")
        plt.show()    
 

if __name__ == '__main__':
    #testing
    pass


