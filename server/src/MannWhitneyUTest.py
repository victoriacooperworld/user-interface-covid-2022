import collections
import os 
from scipy.stats import mannwhitneyu
def form2Arrays(posDir, negDir):
    """
        Input: multiple patient fasta files
    """
    pos = collections.defaultdict(list)
    neg = collections.defaultdict(list)
    for file in os.listdir(posDir):
        tetramers = readOneFile(file)
        for tet in tetramers.keys():
            pos[tet].append(tetramers[tet])

    for file in os.listdir(negDir):
        tetramers = readOneFile(file)
        for tet in tetramers.keys():
            neg[tet].append(tetramers[tet])

    res = collections.defaultdict(float)
    for tet in pos.keys():
        if tet not in neg.keys():
            print(tet + "Not in neg!")
            continue
        else:
            array1, array2 = pos[tet],neg[tet]
            pValue = mannwhitneyu(array1, array2)
            res[tet]=pValue
    return res
            


def readOneFile(path):
    tetramers = collections.defaultdict(float)
    total = 0
    with open(path,"r") as f:
        while True:
            header = f.readline()
            if not header:
                break
            protein =f.readline()
            protein = protein.replace("X","Q")
            freq = int(header.split('_')[-1])
            #sliding window
            total += (len(protein)-3)*freq
            for i in range(len(protein)-3):
                tetramer = protein[i:i+4]
                tetramers[tetramer]+=freq
        
    for key in tetramers.keys():
        tetramers[key]/=total
    return tetramers

                
    
