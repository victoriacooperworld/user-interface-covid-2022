
import csv

import datetime
import logging
import os
import sys
import STetramerNRlarge
from tokenize import String
import pandas as pd
import mysql.connector 
from mysql.connector import Error
#This class has all the query functions to mysql database
        
def FixDelimiters(dirPath, outputDir):
    for file in os.listdir(dirPath):
        filePath = os.path.join(dirPath,file)
        outFilePath = os.path.join(outputDir, file)
        print(dirPath, file)
        with open(filePath,'r') as f:
            with open(outFilePath,'w') as fo:
                while(True):
                    curLine = f.readline()
                    if not curLine:
                        break
                    cur = curLine.split('|')
                    if len(cur) > 3:
                        first = cur[0]
                        last = cur[-1]
                        middle = '!'.join(cur[1:-1])
                        total = '|'.join([first, middle, last])
                        fo.write(total)
                    else:
                        fo.write(curLine)
class databaseInit:

    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            #change the username and password to your own
            host="database-human.cmp1ka38123m.us-west-1.rds.amazonaws.com",
            user="cglabe",
            password="123456789"

            
            # host = "localhost",
            # user = "root",
            # password = "123456"
        )

    def create_index(self, tableName,idColumn):
        try:
            cursor = self.mydb.cursor()
            cursor.execute("CREATE INDEX SEQ_IDX ON "+ tableName + " (" + idColumn + ");")
        except Error as e:
            print("Error while connecting to mysql: ",e)
            quit()
    def is_connected(self):
        if self.mydb.is_connected():
            print("DB connected!")
        else:
            print("DB is not connected!")

    def createDB(self, name):
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                cursor.execute("CREATE DATABASE " + name + ";")
                print("ProteinDB is created")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def createTable(self, databaseName, tableName, col_sql):
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                cursor.execute("USE " + databaseName)
                print('Use Database....')
                cursor.execute("DROP TABLE IF EXISTS " + tableName +";")
                print('Creating table....')
                # cursor.execute("CREATE TABLE " + tableName + "(ID VARCHAR(4), Sequence VARCHAR(20), Description VARCHAR(500))") 
                cursor.execute("CREATE TABLE " + tableName + col_sql+";")            
                print(tableName + " is created....")
        except Error as e:
            print("Error while connecting to MySQL in createTable: ", e)

    def insertDataFromCSV(self, path, tableName ):
        f = csv.reader(open(path))
        header = next(f)
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
            for row in f:
                if len(row) == 0: continue
                if row == None: continue
                # row = row[1:] #Every .csv file will have an index column, get rid that column
                col_size = len(row)
                size = ','.join(["%s"]*col_size)
                cursor.execute("USE ProteinDB")
                sql = "INSERT INTO " + tableName + " VALUES (" + size + ")"
                cursor.execute(sql, tuple(row))
                # the connection is not autocommitted by default, so we must commit to save our changes
                self.mydb.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            cursor.close()
            self.mydb.close()

    # data is a tuple that contains what to put into the table
    # this function is used to insert an entry in proteinID
    def insertDataOneProtein(self,data,  tableName):
        try:
            if self.mydb.is_connected():
                try:
                    cursor = self.mydb.cursor()
                    col_size = len(data)
                    size = ','.join(["%s"]*col_size)
                    cursor.execute("USE ProteinDB")
                    sql = "INSERT INTO " + tableName + " VALUES (" + size + ")"
                    cursor.execute(sql,tuple(data))
                    self.mydb.commit()
                except Error as e:
                    print("Error inserting into db: ", e)
                    print("SQL Code: ", sql,tuple(data))

        except Error as e:
            print("Error while connecting to MySQL", e)

    def insertDataFromDict(self, data, tableName, columnName):
        try:
            if self.mydb.is_connected():
                for key,value in data.items():
                #insert val, column
                    cursor = self.mydb.cursor()
                    #INSERT INTO table_name VALUES (value1, value2, value3, ...);
                    #print("INSERT INTO " + tableName + " "+ columnName + " VALUES " + "('"+key+"','"+str(value)[:15]+"','" + "''" + "')" + ";")
                    cursor.execute("USE ProteinDB")
                    cursor.execute("INSERT INTO " + tableName + " "+ columnName + " VALUES " + "('"+key+"','"+str(value)[:15]+"','"  + "')" + ";")
                    #print("Selecting...")
                    self.mydb.commit()
              
        except Error as e:
            print("Error while connecting to MySQL", e)

    def insert(self,tableName, insertValue):
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                #INSERT INTO table_name VALUES (value1, value2, value3, ...);
                # print("INSERT INTO " + tableName + " VALUES " + insertValue + ";")
                cursor.execute("USE ProteinDB")
                cursor.execute("INSERT INTO " + tableName + " VALUES " + insertValue + ";")
                #print("Selecting...")
                self.mydb.commit()
                
              
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            cursor.close()

    def useDB(self, dbName):
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                cursor.execute("USE " + dbName)
        except Error as e:
            print("Error while connecting to MySQL", e)

    #select query
    def search(self, selectColumn, tableName, columnName, targetValue) -> String:
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                cursor.execute("SELECT " + selectColumn + " FROM " + tableName + " WHERE "+ columnName + "=" + targetValue)
                # print("Selecting...")
                return cursor.fetchall()
        except Error as e:
            print("Error while connecting to MySQL", e)


    def update(self, tableName, updateColumn, newValue, columnName, targetValue) -> String:
        try:
            if self.mydb.is_connected():
                cursor = self.mydb.cursor()
                #cursor.execute("USE ProteinDB")
                # print("UPDATE " + tableName + " SET " + updateColumn + " = '" + newValue + "' WHERE " + columnName + " = " + "'" + targetValue + "'" +";")
                cursor.execute("UPDATE " + tableName + " SET " + updateColumn + " = '" + newValue + "' WHERE " + columnName + " = " + "'" + targetValue + "'" +";")
                #print("Updating...")
                self.mydb.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            cursor.close()
    
    #concat query
    def concat(self, tableName, updateColumn, strConcat, columnName, targetValue):
        try:
            if self.mydb.is_connected():
                try:
                    cursor = self.mydb.cursor()
                    cursor.execute("USE ProteinDB")
                    cursor.execute("Update " + tableName + " SET " + updateColumn + " = CONCAT(" +updateColumn + ", '" +strConcat+"') WHERE " + columnName+" = '" + targetValue+"';")
                    self.mydb.commit()
                except Error as e:
                    print("Error updating column: ", e)
                    print("SQL Code: "+ "Update " + tableName + " SET " + updateColumn + " = CONCAT(" +updateColumn + ", '" +strConcat+"') WHERE " + columnName+" = '" + targetValue+"';")
                    quit()
                
        except Error as e:
            print("Trouble connecting to database: ", e)
    
    #load data infile query for massive insertion
    def loadDataInfile(self, filePath, tableName):
        try:
            if self.mydb.is_connected():
                try:
                    cursor = self.mydb.cursor()
                    specifier = " FIELDS TERMINATED BY '" + "|" + "' LINES TERMINATED BY \'\\n\'" 
                    print("LOAD DATA INFILE '"+ filePath +"' INTO TABLE " + tableName+ specifier + ";")
                    cursor.execute("LOAD DATA INFILE '"+ filePath +"' INTO TABLE " + tableName+ specifier + ";")
                    self.mydb.commit()
                    cursor.close()
                except Error as e:

                    print("Error updating column: ", e)
                    quit()
                
        except Error as e:
            print("Trouble connecting to database: ", e)

                        
   
    def insertDataFromTxt_Protein(self, file,tableName):
        self.useDB('Proteindb')
        with open(file) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                data = line.split('|')
       
             
                idx="\""+data[0]+"\""
                key = "\""+data[1]+"\""
                entry = "\""+data[2][:-2]+"\""     
                update_str="("+idx +","+ key + ","+entry+")"         
                self.insert(tableName,update_str)
           
            f.close()

    
    def insertDataFromTxt_Tetramer(self, file,tableName):
        tableName = "TetramerID"
        with open(file) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                data = line.split('|')
                sequence=data[0]
                pos = data[1]
            
                updateColumn = "Entries"
                update_str= pos 
              
                self.concat(tableName,updateColumn, update_str, "sequence", sequence)

            f.close()
    
     #this function is for insert proteinID from txt files to database
    def insertProtein(self,inputDir):
        self.useDB("ProteinDB")
        self.createTable('ProteinID',"(Id varchar(10) , Description mediumtext, Sequence longTEXT)") 
   
        for file in os.listdir(inputDir):
            filePath = os.path.join(inputDir,file)
            st = datetime.datetime.now()
            print("Reading" + file)
            self.insertDataFromTxt_Protein(filePath,"proteinid_NR")
            et = datetime.datetime.now()
            print("Time used for " + file + " is " + str(et-st))

    #this function is for insert tetramerID from txt files to database
    def insertTetramer(self, inputDir):

        #This is a script that initializes the tetramer database
        #column names: sequence, probability, entries
        base_address = os.path.dirname(sys.path[0])
        db = databaseInit()
        self.useDB("ProteinDB")
        # db.createTable('TetramerID_NR',"(Sequence VARCHAR(4), Probability VARCHAR(15), Entries longTEXT)")
        # self.create_index("TetramerID_NR", "Sequence")

        # path = r"InputFiles\Control.csv"
        # controlDict = STetramerNRlarge.readFile(path)
        # res = STetramerNRlarge.generateTetramer(controlDict)
        # logging.info("Start createTotalDb")
        # db.insertDataFromDict(res, "TetramerID","(sequence, probability, entries)")
   


        for file in os.listdir(inputDir):
            filePath = os.path.join(inputDir,file)
            st = datetime.datetime.now()
            print("Reading " + file)
            self.insertDataFromTxt_Tetramer(filePath,"TetramerID")
            et = datetime.datetime.now()
            print("Time used for " + file + " is " + str(et-st))



def insertProteins():
    db = databaseInit()
    db.createTable('HumanDB','ProteinID',"(Id varchar(10) , Description mediumtext, Sequence longTEXT)") 
    inputDir = r"D:\\\Human\\\ProteinID"
    for file in os.listdir(inputDir):
        st = datetime.datetime.now()
        filePath = inputDir+ "\\\\" + file
        print(filePath)
        db.loadDataInfile(filePath,"ProteinID")
        et = datetime.datetime.now()
        print("Time used for "+file+" is " + str(et-st))


def insertTetramers():
    db = databaseInit()
    inputDir = r"D:\\\OutputFiles1\\\TetramerID\\\WithKeys"
    fileNum=60
    for file in os.listdir(inputDir):
        tableName = 'TetramerID'+str(fileNum)
        db.createTable("HumanDB",tableName,"(Sequence VARCHAR(4), Entries longTEXT)")
        st = datetime.datetime.now()
        filePath = inputDir+ "\\\\" + file
        print("starting creating " + tableName)
        db.loadDataInfile(filePath, tableName)
        et = datetime.datetime.now()
        print("Time used for "+" is " + str(et-st))
        fileNum+=1

if __name__ == '__main__':
    db = databaseInit()
    db.is_connected()
    db.useDB("humandb") 
    print(db.search("*", "tetramerid","sequence","'SSSS'"))
    # uncomment to fix the delimiter
    # dirPath = r"D:\OutputFiles2\OutputFiles2\ProteinID"
    # outdir =  r'D:\OutputFiles2\OutputFiles2\ProteinIDFixed'
    # FixDelimiters(dirPath, outdir)
    

