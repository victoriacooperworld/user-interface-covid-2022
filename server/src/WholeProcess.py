import collections
import heapq
from ipaddress import collapse_addresses
from PatientInput import Input
from Patient import PatientProtein
import GenerateDB.STetramerNRlarge as STetramerNRlarge
import os
import GenerateDB.DatabaseInit as DatabaseInit
if __name__ == '__main__':
    # input = Input()

    # outputPath = r'OutputFiles\total.fna'
    # inputPath = r'Test\Part1TestData'
    # data = input.readFNAFile(inputPath,outputPath) 
    

    #deal with the new merged file
    dir = r'E:\COVID NGS 2022\FASTA\POS\ED'
    patientinput = Input()
    data = patientinput.readFNAFile( dir, outputPath = None)
    #checking first and last data member
    print(data[0],data[-1])
    patientData = PatientProtein(data)
    patientData.countTetramers()
    # outDir = r'E:\COVID NGS 2022\FASTA_OUTPUT\POS\ED'
    # patientData.writeToCSV(os.path.join(outDir, 'Tetramers.csv'), sortOutput=True)
    # patientData.calculateExpectedProbability()
    significant_tetramers=[]
    cut_off = 10
    for tet in patientData.tetramers:
        #find significant tetramers
        if patientData.tetramers[tet].freq<cut_off:
            continue
        else:
            significant_tetramers.append([patientData.tetramers[tet].sequence,patientData.tetramers[tet].freq])
    db = DatabaseInit.databaseInit()
    db.useDB("ProteinDB")
    proteinInfo = collections.defaultdict(int)
    for t in significant_tetramers:
        #find significant proteins
        seq = t[0]
        entries = str(db.search("entries","Tetramerid","sequence",seq)[0])
        entry = entries.split('),(')
        entry[-1] = entry[-1][:-7] #fix the last element's form

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
    
#To be turned into a function for processpatient in server.py
def ProcessPatientDir(dirPath, databaseName ):
    pass
        
        
    
    

