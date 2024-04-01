#provided csv files have 16 measurments per second

import sqlite3
import csv
import os 

class CsvDataBase:
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
 
    def __init__(self):
        self.init_db()
        #print("Database in ram created")
    
    def init_db(self):
        self.cursor.execute("CREATE TABLE cows(dataId INTEGER PRIMARY KEY AUTOINCREMENT,cowId INTEGER,cowExtId INTEGER,snsrPos,timeStamp,acc_x,acc_x_g,acc_y,acc_y_g,acc_z,acc_z_g,gyro_x,gyro_y,gyro_z);")
        self.cursor.execute("CREATE TABLE addedFiles(iD INTEGER PRIMARY KEY AUTOINCREMENT, cowId INTEGER, externalId INTEGER, internalId INTEGER, day INTEGER, month INTEGER, filename TEXT);")
        self.db.commit() #commit to database
    
    def clear_db(self):
        try:
            self.cursor.execute("DROP TABLE cows;")
            self.cursor.execute("DROP TABLE addedFiles;")
            self.db.commit()
        except:
            pass

    def addedFiles_add(self,id,exid,inid,d,m,fn):
        dbStr = ("INSERT INTO addedFiles(cowId,externalId,internalId,day,month,filename) VALUES (%s,%s,%s,%s,%s,'%s');") % (id,exid,inid,d,m,fn)
        self.cursor.execute(dbStr)
        self.db.commit()

    def addedFiles_remove(self,id):
        sql = "DELETE FROM addedFiles where cowId = %s" % (id)
        self.cursor.execute(sql)
        self.db.commit()

    def addedFiles(self):
        self.cursor.execute("SELECT  cowId , externalId , internalId, day , month , filename FROM addedFiles;")
        allFiles = self.cursor.fetchall()
        added = []
        for data in allFiles:
            added.append(data)

        return(added)

    def add_csv(self, csvpath):
        filename = csvpath.split("DATA")
        filename = filename [-1]
        _filename = "DATA"
        _filename += filename
        
        if str(csvpath) not in self.addedFiles():
            with open(csvpath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count+= 1 #skip first line of CSV file, Column names are in there
                    elif line_count == 1:
                        tstp = row[15] 
                        tstp = tstp[14:19]
                        cowId = int(row[6])
                        externalId = int(row[7])
                        internalId = int(row[9])
                        a,b,c,d,e = csvpath.split("_")
                        day = int(b)
                        month = int(c)
                        self.cursor.execute('''INSERT INTO cows(cowId,cowExtId,snsrPos,timeStamp,acc_x,acc_x_g,acc_y,acc_y_g,acc_z,acc_z_g,gyro_x,gyro_y,gyro_z) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(row[6],row[7],row[12],tstp,row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24]))
                        indentifier = (cowId,externalId,internalId,day,month,_filename) #return id,intid,extid,day,month,filename
                        line_count += 1
                        
                    else:          
                
                        tstp = row[15] 
                        tstp = tstp[14:19]   #remove date and hours from timestamp
                        line_count += 1
                        self.cursor.execute('''INSERT INTO cows(cowId,cowExtId,snsrPos,timeStamp,acc_x,acc_x_g,acc_y,acc_y_g,acc_z,acc_z_g,gyro_x,gyro_y,gyro_z) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(row[6],row[7],row[12],tstp,row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24]))
            
            
            
            
            
            self.addedFiles_add(cowId,externalId,internalId,day,month,_filename)
            
            return(indentifier)
        else:
            print("This file is already added")
            return(-1)
    
    def remove_by_id(self,id):
        sql = "DELETE FROM cows WHERE cowId = %s;" % (id)
        self.cursor.execute(sql)
        self.db.commit()

        self.addedFiles_remove(id)



    def export_db(self,filename):
    
        def exportit():
            try:

                dbfile = filename
                if os.path.exists(dbfile):
                    os.remove(dbfile) # remove last db dump

                new_db = sqlite3.connect(dbfile)
                c = new_db.cursor() 
                c.executescript("\r\n".join(self.db.iterdump()))
                new_db.close()
                print("Data Saved Sucessfully")
                return(1)
            except:
                raise RuntimeError("Error has ocured,make sure file",filename," is closed")

        exportit()

    def load_db(self,filename):
        
        def loadit():
            try:
                self.clear_db()
                dbfile = filename
                new_db = sqlite3.connect(dbfile)
                c = self.db.cursor() 
                c.executescript("\r\n".join(new_db.iterdump()))
                new_db.close()
                print("Data Imported Sucessfully")
                
            except:
                raise RuntimeError("Error has ocured,make sure file",filename," is closed")

        loadit()
        return(self.addedFiles())
       
            
 
    def getAccel(self,id,column = "acc_x_g"):
        
        limb = "RF"
        #limb = "LF"
        #lib = "Ear"
        #column = "acc_x_g"
        #column = "acc_y_g"
        #column = "acc_x"
        #column = "acc_y"
        queryStr = "SELECT %s  FROM cows WHERE (cowId = '%s' AND snsrPos = '%s' );" % (column,id,limb)
        #print(queryStr)
        self.cursor.execute(queryStr)
        all_rows = self.cursor.fetchall()

        if not all_rows : #return is empty
            raise Exception("ID not in database or invalid column name.")
            
        
        dict = []
        for row in all_rows: # row[0] returns the first column in the query    
            a = (float(row[0]))
            dict.append(a)

        return (dict)