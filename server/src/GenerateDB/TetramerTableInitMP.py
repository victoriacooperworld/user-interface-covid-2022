from multiprocessing import Pool
import multiprocessing
from GenerateDB.DatabaseInit import databaseInit

from timeit import timeit
import GenerateDB.STetramerNRlarge as STetramerNRlarge
import os
import sys
import logging
from mysql.connector import pooling

def initialize_database():
    """
    This is a script that initializes the tetramer database
    column names: sequence, probability, entries
    """


    base_address = os.path.dirname(sys.path[0])
    db = databaseInit()
    #db.createDB()



    #db.createTable('TetramerID',"(Sequence VARCHAR(4), Probability VARCHAR(50), Entries VARCHAR(100000))") 
    db.createTable('TetramerID',"(Sequence VARCHAR(4), Probability VARCHAR(15), Entries VARCHAR(16000))")
    db.create_index("tetramerid", "Sequence")

    #db.createTable('ProteinID',"(PID VARCHAR(60), Description mediumtext, Sequence longTEXT)") 
    db.createTable('ProteinID',"(Id int NOT NULL AUTO_INCREMENT , Description mediumtext,Sequence longTEXT ,PRIMARY KEY (Id) )") 
    #db.create_index("proteinid", "Description")


    numCores = multiprocessing.cpu_count()
    logging.critical("Operating on ", numCores, " cores")
    #connection_pool = pooling.MySQLConnectionPool(pool_name = "connectionPool",
    #                                                pool_size =numCores,
    #                                                pool_reset_session=True,
    #                                                host = 'localhost',
    #                                                database = 'ProteinDB',
    #                                                user = 'root',
    #                                                password= '123456')

    

    path = r"InputFiles\Control.csv"
    controlDict = STetramerNRlarge.readFile(path)
    res = STetramerNRlarge.generateTetramer(controlDict)
    db.insertDataFromdict(res, "TetramerID","(sequence, probability, entries)")
    #STetramerNRlarge.createTetramerDB( f"{base_address}\\InputFiles\\NR_Data", 'TetramerID')
    #STetramerNRlarge.createTetramerDB(r"E:\Non-redundantProteome\nr", db, 'TetramerID')
    logging.info("Start createTotalDb")

    #STetramerNRlarge.CreateIDList(f"{base_address}\\InputFiles\\NR_Data", db, 'ProteinID')
    #STetramerNRlarge.CreateIDList(r"E:\Non-redundantProteome\nr", db, 'ProteinID')
    #STetramerNRlarge.CreateTotalDB(f"{base_address}\\InputFiles\\NR_Data", db, "TetramerId", "ProteinId")
    
    argList = []
    for i in range(0,16):
        #newdb = databaseInit(connection_pool.get_connection())
        
        argList.append([f"{base_address}\\InputFiles\\NR_Data",  'TetramerId','ProteinId', i, 87])
    with Pool(16) as p:
        p.starmap(STetramerNRlarge.CreateTotalDB_MP,argList)

    logging.info(f"Finished CreateTotalDb")


initialize_database()
#argList = []
#for i in range 0 16:
#arglist.append([DirName,db,tetTableName, proteinTableName, i])
#with Pool(16) as p:
# p.map(CreateTotalDB_MP,)
#multiprocessed createtotalmp