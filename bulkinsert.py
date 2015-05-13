#
# Open addresses ETL Common Library
# 
# Bulk Insert Class
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Bulk insert items into a MySQl or MariaDB table
#
# Arguments:    database cursor, table name, list of fields, max =  maximum buffer (2000), ignore = ingore duplicate keys (false)
#

import MySQLdb
import string
import sys
import chardet

class BulkInsert:

    def __init__(self, cur,table,fields,max=2000,ignore=False):        # Instantiation - pass database
        self.max_rows = max
        self.cursor = cur
        self.fields = fields
        self.table = table
        if ignore:
            self.type = "IGNORE "
        else:
            self.type = ""
        self.nrecs = 0
        self.bufrecs = 0
        self.values = []
        self.prefix = u"INSERT "+self.type+"INTO `"+self.table+"` (" 
        self.prefix += string.join(["`" + field + "`" for field in fields],",")
        self.prefix += ") VALUES "
        
    def close(self):
        if self.bufrecs > 0:
            self.writeData()
            
    def addRow(self,row):
        self.values.append(row)
        self.nrecs += 1
        self.bufrecs += 1
        if (self.nrecs % self.max_rows) == 0:
            self.writeData()

    def writeData(self):
        query = self.prefix
        for i in range(0,len(self.values)):
            if i > 0:
                query += ", "
            query += "("
            for j in range(0,len(self.fields)):
                if j > 0:
                    query += ", "
                if not isinstance(self.values[i][j], (str, unicode)):  # Is not string
                    query += "'" + str(self.values[i][j]) + "'"                
                elif self.values[i][j] == "NULL":
                    query += "NULL"
                elif self.values[i][j][0:12] == "GeomFromText":
                    query += self.values[i][j]
                else:
                    try:
                        if self.values[i][j] == '':
                            value = u''
                        else:
                            charset = chardet.detect(self.values[i][j])['encoding']
                            value = unicode(self.values[i][j].decode(charset).replace(u"'",u"\\'"))
                        query += u"'" + value + u"'"
                    except Exception, e:
                        print query
                        print self.values[i]
                        print chardet.detect(self.values[i][j])
                        print e
                        sys.exit(1)
            query += ")"
        query += ";"
        # print query
        try:
            self.cursor.execute(query)
        except Exception, e:
            print query
            print e
            print chardet.detect(query)
            sys.exit(1)
        self.values = []
        self.bufrecs = 0
