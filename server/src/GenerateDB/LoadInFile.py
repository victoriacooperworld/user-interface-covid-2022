#load in tetramerid


from datetime import datetime
import sys
import DatabaseInit
import os
import STetramerNRlarge
import main





base_address = os.path.dirname(sys.path[0])
pathControl = f"{base_address}\..\InputFiles\Control.csv"
controlDict = STetramerNRlarge.readFile(pathControl)
res = STetramerNRlarge.generateTetramer(controlDict)
path = r'D:\OutputFiles1\TetramerID\Merged\Merged\key.txt'
main.MakeKeyColumn(path, res)
tetramersDir = r'D:\OutputFiles1\TetramerID\Merged\Merged'
outputTetramersDir = r'D:\OutputFiles1\TetramerID\WithKeys'

#Merged tetramer id files with a key 
for file in os.listdir(tetramersDir):
    st = datetime.now()
    pathName = os.path.join(tetramersDir, file)
    outputPath = os.path.join(outputTetramersDir,file)
    print(pathName, outputPath)
    main.mergeTxt( path, pathName,outputPath, deletePath2 = True)
    et=datetime.now()
    print("Time used: "+str(et-st))
