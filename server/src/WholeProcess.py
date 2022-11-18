import collections
import heapq
from ipaddress import collapse_addresses
from PatientInput import Input
from Patient import PatientProtein
import GenerateDB.STetramerNRlarge as STetramerNRlarge
import os
import GenerateDB.DatabaseInit as DatabaseInit
from scipy.stats import mannwhitneyu

#reads in a directory of patient data and cuts off tetramers with less than a given number in frequency
def ReadTetramersCutoff(dirName, cutoff=2):
    #deal with the new merged file
    dir = dirName
    patientinput = Input()
    data = patientinput.readFNAFile( dir, outputPath = None)
    print(data[0],data[-1])
    patientData = PatientProtein(data)
    patientData.countTetramers()
    above_cutoff=[]
    cut_off = cutoff
    for tet in patientData.tetramers:
        #find significant tetramers
        if patientData.tetramers[tet].freq<cut_off:
            continue
        else:
            above_cutoff.append([patientData.tetramers[tet].sequence,patientData.tetramers[tet].freq])
    return above_cutoff
    

def GetSignificant(Pos, Neg, method = 'MWU'):
    res = mannwhitneyu(Pos,Neg, axis=2,alternative='two-sided')

if __name__ == '__main__':

    PosTets = ReadTetramersCutoff(r'C:\Users\User\Desktop\Alzheimers\AD')
    NegTets = ReadTetramersCutoff(r'C:\Users\User\Desktop\Alzheimers\NC')

    print(PosTets)
    print(NegTets)
    quit()
    #INSERT CODE TO filter significant tetramers using mann whitney/etc
    #and then correct by bonferroni and/or other for false discovery
    significant_tetramers = MannWhitneyU()
    ########


    #This is the code used to create a list of proteins once we have the significant tetramers
    db = DatabaseInit.databaseInit()
    db.useDB("ProteinDB")
    proteinInfo = collections.defaultdict(int)
    for t in significant_tetramers:
        #find significant proteins

        # get the tetramer's sequence
        seq = t[0]
        # get the entries in tetramerID
        entries = str(db.search("entries","Tetramerid","sequence",seq)[0]) 
        entry = entries.split('),(')
        entry[-1] = entry[-1][:-7] #fix the last element's form

        # calculate the hit for each proteins
        for e in entry:
            e=e[3:]
            data = e.split(',')
            proteinInfo[data[0]]+=1
   
    #filter non-significant proteins
    # print(proteinInfo.values())

    # heap sort for the top 100
    heap = []
    heap_size = 100

    for k,v in proteinInfo.items():
        heapq.heappush(heap,(v,k))
        if len(heap)>heap_size:
            heapq.heappop(heap)
    
    res_protein = []
    for pair in heap:
        print(pair)
        idx = pair[1]
        res_protein.append(idx)
    ret = []
    # start to query from db
    for protein_idx in res_protein:
        des = db.search("description","proteinid","id",str(protein_idx))
        ret.append(des)
    
    for i in ret:
        print(i)
    

    
    
        
        
    
    

