import collections
import os 
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
import pandas as pd
import dash  
import dash_bio as dashbio  
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
    res1 = collections.defaultdict(list)
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
            #order, however, does not affect pvalue.

            # mannWhitneyObject = mannwhitneyu( pos[tet] ,EmptyArr)

            # statistic = mannWhitneyObject.statistic
            # ##
            mannWhitneyObject = mannwhitneyu(EmptyArr,pos[tet])
            statistic = (nPosStatistic - mannWhitneyObject.statistic)/numPosPatients
            # ###

            pValue = mannWhitneyObject.pvalue
            res[tet].append(statistic)
            res[tet].append(pValue)

            mannWhitneyObject1 = mannwhitneyu(pos[tet],EmptyArr)
            statistic1 = (nNegStatistic - mannWhitneyObject1.statistic)/numNegPatients
            res1[tet].append(statistic1)
            res1[tet].append(pValue)

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

            # mannWhitneyObject = mannwhitneyu( EmptyArr,neg[tet])
            # statistic = mannWhitneyObject.statistic
            # ##TEST CODE
            mannWhitneyObject = mannwhitneyu( neg[tet],EmptyArr)
            # print("Statistic is ", mannWhitneyObject.statistic)
            statistic = (nPosStatistic - mannWhitneyObject.statistic)/numPosPatients

            # ###
            pValue = mannWhitneyObject.pvalue
            res[tet].append(statistic)
            res[tet].append(pValue)

            mannWhitneyObject1 = mannwhitneyu(EmptyArr, neg[tet])
            statistic1 = (nNegStatistic - mannWhitneyObject1.statistic)/numNegPatients
            res1[tet].append(statistic1)
            res1[tet].append(pValue)
            numOutNeg+=1
            continue
        else:
            
            neg[tet] = neg[tet] + ([0] * (numNegPatients-len(neg[tet])))
            pos[tet] = pos[tet] + ([0] * (numPosPatients-len(pos[tet])))
            array1, array2 = pos[tet],neg[tet]
            if len(neg[tet]) != numNegPatients or len(pos[tet]) != numPosPatients:
                print("INEQUAL LENGTH: QUITTING")
                quit()
            
            # mannWhitneyObject = mannwhitneyu(array1, array2)
            # statistic = mannWhitneyObject.statistic
            # ###TEST CODE
            mannWhitneyObject = mannwhitneyu(array2,array1)
            statistic = (nPosStatistic - mannWhitneyObject.statistic)/numPosPatients
            # ###

            pValue = mannWhitneyObject.pvalue
            res[tet].append(statistic)
            res[tet].append(pValue)

            mannWhitneyObject1 = mannwhitneyu(array1,array2)
            statistic1 = (nNegStatistic - mannWhitneyObject1.statistic)/numNegPatients
            res1[tet].append(statistic1)
            res1[tet].append(pValue)

            numIn+=1
            continue
    print("There are ", numIn," in both and ", numOutPos, " only in Pos and ", numOutNeg, " only in Neg")
    return res, res1
            

 
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
            try:
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
            except ValueError:
                print("Header is ", header, " and protein is ", protein, "at path ", path)
                continue
        
    for key in tetramers.keys():
        tetramers[key]/=total
    return tetramers

# NOTE: DOES NOT alter tetdict, returns an adjusted copy of tetdict
def FalseDiscoveryCorrection(tetDict, method = 'fdr_tsbky'):
    # print('method is', method)
    newDict = tetDict
    Pvals = []
    for pvalue in newDict.values():
        Pvals.append(pvalue[1])

    #returns an object with lots of relevant info
    correctedPvals = multipletests(Pvals, method = method, returnsorted=False)
    correctedPvals = correctedPvals[1]
    # print(newDict.keys[0],newDict.keys[-1] )
    # print(correctedPvals[0],correctedPvals[-1])
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



#function that returns a sorted 2d array from a dict assuming dict values are numbers
def sortTets(tetDict, method = 'getStatistict'):
    arr = list(tetDict.items())
    if method == 'getStatistic':
        #get by largest statistic in positive group
        arr.sort(key = getStatistic, reverse = True)
    elif method == 'getPValue':
        #sort by smallest pvalue
        arr.sort(key = getPValue)
    else:
        print("ERROR: INVALID METHOD IN SortTets")
        quit()
    return arr


#The main function used
def getSigTets(posDir,negDir, cutoff = 2, qCutoff = 0.01, topHits = 20):
    res, res1 = form2Arrays(posDir,negDir, cutoff=cutoff)

    numSig = 0
    for tet, value in res.items():
        if value[1] < .05:
            numSig+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    print("Number of significant tet in pos before correction: ", numSig)
    
    numSig1 = 0
    for tet, value in res1.items():
        if value[1] < .05:
            numSig1+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    print("Number of significant tet in Neg before correction: ", numSig1)

    correctedRes = FalseDiscoveryCorrection(res, method = 'fdr_tsbky')
    correctedRes1 = FalseDiscoveryCorrection(res1, method = 'fdr_tsbky')
    #all significant tets
    numSig=0
    # finalList = list(correctedRes.items())
    sortedTets = sortTets(correctedRes, method = 'getStatistic')
    sortedTets1 = sortTets(correctedRes1, method = 'getStatistic')
    # for i in range(0,20):
    #     print(sortedTets[i])


    #outputting to a csv
    outputList = []
    for tetEntry in sortedTets:
        if(tetEntry[1][2]<qCutoff):
            outputList.append([tetEntry[0],tetEntry[1][0],tetEntry[1][1],tetEntry[1][2] ])

    outputList1 = []
    for tetEntry1 in sortedTets1:
        if(tetEntry1[1][2]<qCutoff):
            outputList.append([tetEntry1[0], tetEntry1[1][0], tetEntry1[1][1], tetEntry1[1][2] ])
        
    df = pd.DataFrame(outputList, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    df.to_csv(r'C:\Users\User\Desktop\BrucellaData\ADNC_SigTetramersPos.csv')

    df1 = pd.DataFrame(outputList1, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    df1.to_csv(r'C:\Users\User\Desktop\BrucellaData\ADNC_SigTetramersNeg.csv')

    outPath = r'C:\Users\User\Desktop\BrucellaData\Top20_ADNC_SigTetramersPos.txt'
    outpath1 = r'C:\Users\User\Desktop\BrucellaData\Top20_ADNC_SigTetramersNeg.txt'
    with open(outPath,'w') as f:
        for i in range (0,topHits):
            tetEntry = sortedTets[i]
            f.write(str(tetEntry[0]) +'\t'+str(tetEntry[1][2])+'\n')
    with open(outpath1,'w') as f:
        for i in range (0,topHits):
            tetEntry1 = sortedTets1[i]
            f.write(str(tetEntry1[0]) +'\t'+str(tetEntry1[1][2])+'\n')

    outputList2=[]
    for tetramer in correctedRes.keys():
        if correctedRes[tetramer][1] < qCutoff:
            outputList2.append([tetramer, correctedRes[tetramer][0] - correctedRes1[tetramer][0], correctedRes[tetramer][1], "NA" ])

    df2 = pd.DataFrame(outputList2, columns = ["GENE", "EFFECTSIZE", "P", "SNP"])
    # df2.to_csv(r'C:\Users\User\Desktop\BrucellaData\VolcPlot.csv')

    figureOut = dashbio.VolcanoPlot(
        dataframe = df2
    )
    figureOut.show()
    dash.dcc.Graph(figure = figureOut)
    outputPath2 = r'C:\Users\User\Desktop\BrucellaData\VolcanoPlot.html'
    with open(outputPath2, 'w') as f:
        f.write(figureOut.to_html(full_html = False, include_plotlyjs='cdn'))

    return outPath, outpath1, outputPath2



if __name__ == '__main__':
    # res = form2Arrays(r'C:\Users\User\Desktop\BrucellaData\Fasta\Brucella NGS 2022\Pos\CultureSeraPos',r'C:\Users\User\Desktop\BrucellaData\Fasta\Brucella NGS 2022\Neg', cutoff=2)
    res, res1 = form2Arrays(r'C:\Users\User\Desktop\Alzheimers\AD',r'C:\Users\User\Desktop\Alzheimers\NC', cutoff=2)

    numSig = 0
    for tet, value in res.items():
        if value[1] < .05:
            numSig+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    print("Number of significant tet in pos before correction: ", numSig)
    
    numSig1 = 0
    for tet, value in res1.items():
        if value[1] < .05:
            numSig1+=1
        if len(value) != 2:
            print("ERROR: MISSING STATISTIC OR PVALUE: ", value) 
    print("Number of significant tet in pos before correction: ", numSig1)

    correctedRes = FalseDiscoveryCorrection(res, method = 'fdr_tsbky')
    correctedRes1 = FalseDiscoveryCorrection(res1, method = 'fdr_tsbky')
    #all significant tets
    numSig=0
    # finalList = list(correctedRes.items())
    sortedTets = sortTets(correctedRes, method = 'getStatistic')
    sortedTets1 = sortTets(correctedRes1, method = 'getStatistic')
    # for i in range(0,20):
    #     print(sortedTets[i])


    #outputting to a csv
    outputList = []
    for tetEntry in sortedTets:
        if(tetEntry[1][2]<.01):
            outputList.append([tetEntry[0],tetEntry[1][0],tetEntry[1][1],tetEntry[1][2] ])

    outputList1 = []
    for tetEntry1 in sortedTets1:
        if(tetEntry1[1][2]<.01):
            outputList1.append([tetEntry1[0], tetEntry1[1][0], tetEntry1[1][1], tetEntry1[1][2] ])
        
    df = pd.DataFrame(outputList, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    df.to_csv(r'C:\Users\User\Desktop\BrucellaData\ADNC_SigTetramersPos.csv')

    df1 = pd.DataFrame(outputList1, columns = ['Tetramer', 'Statistic by AD', 'P Value', 'Q Value']).set_index('Tetramer')
    df1.to_csv(r'C:\Users\User\Desktop\BrucellaData\ADNC_SigTetramersNeg.csv')

    outPath = r'C:\Users\User\Desktop\BrucellaData\Top20_ADNC_SigTetramersPos.txt'
    outpath1 = r'C:\Users\User\Desktop\BrucellaData\Top20_ADNC_SigTetramersNeg.txt'
    with open(outPath,'w') as f:
        for i in range (0,20):
            tetEntry = sortedTets[i]
            f.write(str(tetEntry[0]) +'\t'+str(tetEntry[1][2])+'\n')
    with open(outpath1,'w') as f:
        for i in range (0,20):
            tetEntry1 = sortedTets1[i]
            f.write(str(tetEntry1[0]) +'\t'+str(tetEntry1[1][2])+'\n')

    outputList2=[]
    for tetramer in correctedRes.keys():
        if correctedRes[tetramer][1] < .01:
            outputList2.append([tetramer, correctedRes[tetramer][0] - correctedRes1[tetramer][0], correctedRes[tetramer][1], "NA" ])

    df2 = pd.DataFrame(outputList2, columns = ["GENE", "EFFECTSIZE", "P", "SNP"])
    # df2.to_csv(r'C:\Users\User\Desktop\BrucellaData\VolcPlot.csv')

    figureOut = dashbio.VolcanoPlot(
        dataframe = df2
    )
    figureOut.show()
    dash.dcc.Graph(figure = figureOut)

    with open(r'C:\Users\User\Desktop\BrucellaData\ADNCPlot.html', 'w') as f:
        f.write(figureOut.to_html(full_html = False, include_plotlyjs='cdn'))

    print(outPath, outpath1) 
