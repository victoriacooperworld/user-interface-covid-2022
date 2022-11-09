import collections
import os 
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
def form2Arrays(posDir, negDir, cutoff = 10):
    """
        Input: multiple patient fasta files
    """
    pos = collections.defaultdict(list)
    neg = collections.defaultdict(list)
    for file in os.listdir(posDir):
        tetramers = readOneFile(os.path.join(posDir,file), cutoff = cutoff)
        for tet in tetramers.keys():
            pos[tet].append(tetramers[tet])

    for file in os.listdir(negDir):
        tetramers = readOneFile(os.path.join(negDir,file), cutoff = cutoff)
        for tet in tetramers.keys():
            neg[tet].append(tetramers[tet])

    res = collections.defaultdict(float)
    numIn = 0
    numOutPos = 0
    numOutNeg = 0
    for tet in pos.keys() | neg.keys():
        if tet not in neg.keys() and tet in pos.keys():
            # print(tet + " Not in neg!")
            numOutPos+=1
            pvalue = mannwhitneyu([0], pos[tet]).pvalue
            res[tet] = pvalue
            continue
        elif tet not in pos.keys() and tet in neg.keys():
            # print(tet + " Not in pos!")
            numOutNeg+=1
            pValue = mannwhitneyu([0], neg[tet]).pvalue
            res[tet]=pValue
            continue
        else:
            array1, array2 = pos[tet],neg[tet]
            pValue = mannwhitneyu(array1, array2).pvalue
            res[tet]=pValue
            numIn+=1
            continue
    print("There are ", numIn," in both and ", numOutPos, " only in Pos and ", numOutNeg, " only in Neg")
    return res
            

 
def readOneFile(path, cutoff = 0):
    tetramers = collections.defaultdict(float)
    total = 0
    with open(path,"r") as f:
        while True:
            header = f.readline()
            # print(header)
            if not header:
                break
            protein =f.readline()
            protein = protein.replace("X","Q")
            protein = protein.rstrip('\n')
            freq = int(header.split('_')[-1])
            if freq < cutoff:
                continue
            #sliding window
            total += (len(protein)-3)*freq
            for i in range(len(protein)-3):
                tetramer = protein[i:i+4]
                tetramers[tetramer]+=freq
        
    for key in tetramers.keys():
        tetramers[key]/=total
    return tetramers

#NOTEE: DOES NOT alter tetdict, returns an adjusted copy of tetdict
def FalseDiscoveryCorrection(tetDict, method = 'bonferroni'):
    newDict = tetDict
    Pvals = []
    for pvalue in newDict.values():
        Pvals.append(pvalue)
    
    #returns an object with lots of relevant info
    correctedPvals = multipletests(Pvals, method = method)

    correctedPvals = correctedPvals[1]

    if len(correctedPvals) != len(newDict):
        print("UNKNOWN ERROR: PVALS SIZE DOES NOT MATCH DICT SIZE")
        quit()
    index = 0
    for key in newDict.keys():
        newDict[key] = correctedPvals[index]
        index+=1
    return newDict



if __name__ == '__main__':
    res = form2Arrays('/Users/keanewong/Desktop/Kmer/AD_NC/Positive','/Users/keanewong/Desktop/Kmer/AD_NC/Negative')

    # print(res)
    for tet, value in res.items():
        if value < .05:
            print(tet)
    
    correctedRes = FalseDiscoveryCorrection(res, method = 'bonferroni')
    # print(correctedRes)
    #all significant tets
    print("Corrected for false discovery:")
    for tet, value in correctedRes.items():
        if value < .05:
            print(tet)
    
