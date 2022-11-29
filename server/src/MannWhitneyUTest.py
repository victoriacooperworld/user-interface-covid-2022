import collections
import os 
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
import pandas as pd
def form2Arrays(posDir, negDir, cutoff = 0):
    """
        Input: multiple patient fasta files
    """
    pos = collections.defaultdict(list)
    neg = collections.defaultdict(list)
    numPosPatients = 0
    for file in os.listdir(posDir):
        tetramers = readOneFile(os.path.join(posDir,file), cutoff = cutoff)
        numPosPatients+=1
        for tet in tetramers.keys():
            pos[tet].append(tetramers[tet])

    numNegPatients = 0
    for file in os.listdir(negDir):
        tetramers = readOneFile(os.path.join(negDir,file), cutoff = cutoff)
        numNegPatients+=1
        for tet in tetramers.keys():
            neg[tet].append(tetramers[tet])

    res = collections.defaultdict(list)
    numIn = 0
    numOutPos = 0
    numOutNeg = 0
    nNegStatistic = numNegPatients*numPosPatients + numNegPatients*(numNegPatients+1)/2
    nPosStatistic = numPosPatients*numNegPatients + numPosPatients*(numPosPatients+1)/2
    for tet in pos.keys() | neg.keys():
        if tet not in neg.keys() and tet in pos.keys():
            
            #signals that none of the negative patients had it
            EmptyArr = [0] * numNegPatients
            #this ensures that for tetramer tet, pos[tet] has a length equal to the number of patients
            #the [0] elements represents that some positive patients didnt have that tetramer
            pos[tet] = pos[tet] + ([0] * (numPosPatients-len(pos[tet])))
            if len(EmptyArr) != numNegPatients or len(pos[tet]) != numPosPatients:
                print("INEQUAL LENGTH: QUITTING")
                quit()
            #MAKE SURE that the positive group is first to make sure the outputstatistic is of the positive group
            #order, howeever, does not affect pvalue.

            mannWhitneyObject = mannwhitneyu( pos[tet] ,EmptyArr)
            # ##TEST CODE
            # mannWhitneyObject = mannwhitneyu(EmptyArr,pos[tet])
            # statistic = nPosStatistic - mannWhitneyObject.statistic

            # ###

            pValue = mannWhitneyObject.pvalue
            statistic = mannWhitneyObject.statistic
            res[tet].append(statistic)
            res[tet].append(pValue)
            numOutPos+=1
            continue
        elif tet not in pos.keys() and tet in neg.keys():
            
            #Empty Arr signals that none of the positive patients had it
            EmptyArr = [0] * numPosPatients
            #this ensures that for tetramer tet, neg[tet] has a length equal to the number of patients
            #the [0] elements represents that some negative patients didnt have that tetramer
            neg[tet] = neg[tet] + ([0] * (numNegPatients-len(neg[tet])))
            if len(EmptyArr) != numPosPatients or len(neg[tet]) != numNegPatients:
                print("INVALID LENGTH: QUITTING")
                quit()
            #MAKE SURE that the positive group is first to make sure the outputstatistic is of the positive group
            #order, howeever, does not affect pvalue.

            mannWhitneyObject = mannwhitneyu( EmptyArr,neg[tet])
            # ##TEST CODE
            # mannWhitneyObject = mannwhitneyu( neg[tet],EmptyArr)
            # # print("Statistic is ", mannWhitneyObject.statistic)
            # statistic = nPosStatistic - mannWhitneyObject.statistic

            # ###
            pValue = mannWhitneyObject.pvalue
            statistic = mannWhitneyObject.statistic
            res[tet].append(statistic)
            res[tet].append(pValue)
            numOutNeg+=1
            continue
        else:
            array1, array2 = pos[tet],neg[tet]
            neg[tet] = neg[tet] + ([0] * (numNegPatients-len(neg[tet])))
            pos[tet] = pos[tet] + ([0] * (numPosPatients-len(pos[tet])))
            if len(neg[tet]) != numNegPatients or len(pos[tet]) != numPosPatients:
                print("INEQUAL LENGTH: QUITTING")
                quit()
            
            mannWhitneyObject = mannwhitneyu(array1, array2)
            # ###TEST CODE
            # mannWhitneyObject = mannwhitneyu(array2,array1)

            # statistic = nPosStatistic - mannWhitneyObject.statistic
            # ###

            pValue = mannWhitneyObject.pvalue
            statistic = mannWhitneyObject.statistic
            res[tet].append(statistic)
            res[tet].append(pValue)
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
            # protein = protein.replace("X","Q")
            protein = protein.rstrip('\n')
            freq = int(header.split('_')[-1])
            if freq <= cutoff:
                continue
            #sliding window
            total += (len(protein)-3)*freq
            for i in range(len(protein)-3):
                tetramer = protein[i:i+4]
                if 'X' in tetramer:
                    continue
                else:
                    tetramers[tetramer]+=freq
        
    for key in tetramers.keys():
        tetramers[key]/=total
    return tetramers

#NOTEE: DOES NOT alter tetdict, returns an adjusted copy of tetdict
def FalseDiscoveryCorrection(tetDict, method = 'fdr_tsbky'):
    print('method is', method)
    newDict = tetDict
    Pvals = []
    for pvalue in newDict.values():
        Pvals.append(pvalue[1])

    #returns an object with lots of relevant info
    correctedPvals = multipletests(Pvals, method = method, returnsorted=False)
    correctedPvals = correctedPvals[1]
    # print(newDict.keys[0],newDict.keys[-1] )
    print(correctedPvals[0],correctedPvals[-1])
    if len(correctedPvals) != len(newDict):
        print("UNKNOWN ERROR: PVALS SIZE DOES NOT MATCH DICT SIZE")
        quit()
    index = 0
    # quit()
    for key in newDict.keys():
        newDict[key].append(correctedPvals[index])
        index+=1
    return newDict

def getStatistic(pair):
    return pair[1][0]

def getPValue(pair):
    return pair[1][1]

def getQValue(pair):
    return pair[1][2]

#function that returns a sorted 2d array from a dict assuming dict values are numbers
def sortTets(tetDict, method = 'getStatistict'):
    arr = list(tetDict.items())
    if method == 'getStatistic':
        #get by largest statistic in positive group
        arr.sort(key = getStatistic, reverse = True)
    elif method == 'getPValue':
        #sort by smallest pvalue
        arr.sort(key = getPValue)
    elif method == 'getQValue':
        #sort by smallest qvalue
        arr.sort(key = getQValue)
    else:
        print("ERROR: INVALID METHOD IN SortTets")
        quit()
    return arr


#The main function used
def getSigTets(posDir,negDir, numReturns,cutoff = 0):
    res = form2Arrays(posDir,negDir, cutoff=cutoff)

    numSig = 0
    for tet, value in res.items():
        if value[1] < .05:
            numSig+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    
    print("Number of significant tet before correction: ", numSig)
    
    correctedRes = FalseDiscoveryCorrection(res, method = 'fdr_tsbky')
    #all significant tets
    numSig=0
    # finalList = list(correctedRes.items())
    sortedTets = sortTets(correctedRes, method = 'getStatistic')

    #purging out only the significant q valued tetramers
    significantTetsOnly = []
    for entry in sortedTets:
        if entry[1][2] > 0.05:
            continue
        else:
            significantTetsOnly.append(entry)
    sortedTets = significantTetsOnly

    #outputting to a csv
    outputList = []
    for tetEntry in sortedTets:
        outputList.append([tetEntry[0],tetEntry[1][0],tetEntry[1][1],tetEntry[1][2] ])
    # df = pd.DataFrame(outputList, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    # df.to_csv('/Users/keanewong/Desktop/Kmer/AD_NC/ADNC_SigTetramers.csv')
    outputList2 = []
    for i in range (0,20):
        tetEntry = sortedTets[i]
        outputList2.append([tetEntry[0],tetEntry[1][2]])
    return outputList2



if __name__ == '__main__':
    res = form2Arrays('/Users/keanewong/Desktop/Kmer/AD_NC/Positive','/Users/keanewong/Desktop/Kmer/AD_NC/Negative', cutoff=0)

    numSig = 0
    for tet, value in res.items():
        if value[1] < .05:
            numSig+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    
    print("Number of significant tet before correction: ", numSig)
    
    correctedRes = FalseDiscoveryCorrection(res, method = 'fdr_tsbky')
    #all significant tets
    numSig=0
    # finalList = list(correctedRes.items())
    sortedTets = sortTets(correctedRes, method = 'getStatistic')
    for i in range(0,20):
        print(sortedTets[i])

    #purging out only the significant q valued tetramers
    significantTetsOnly = []
    for entry in sortedTets:
        if entry[1][2] > 0.05:
            continue
        else:
            significantTetsOnly.append(entry)
    sortedTets = significantTetsOnly

    #outputting to a csv
    outputList = []
    for tetEntry in sortedTets:
        outputList.append([tetEntry[0],tetEntry[1][0],tetEntry[1][1],tetEntry[1][2] ])
    df = pd.DataFrame(outputList, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    df.to_csv('/Users/keanewong/Desktop/Kmer/AD_NC/ADNC_SigTetramers.csv')
    outputList2 = []
    with open('/Users/keanewong/Desktop/Kmer/AD_NC/Top20_ADNC_SigTetramers.csv','w') as f:
        for i in range (0,20):
            tetEntry = sortedTets[i]
            f.write(str(tetEntry[0]) +'\t'+str(tetEntry[1][2])+'\n')
