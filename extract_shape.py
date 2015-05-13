# 
# Fusion Data Science Mesh Library
# Extract Data from Shapefile Class
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       (c) Fusion Data Science Limited 2014
#
# Purpose       Extract shapes and attributes from shapefile
#

import shapefile
import datetime
import collections

class shapeExtract:

    def __init__(self, file):   # Instantiation - takes file as a string argument
        self.sf = shapefile.Reader(file)
        self.points = self.sf.shapes()
        self.records = self.sf.records()
        self.fields = self.sf.fields
        
    def getTableSQL(self, table):
        query = "CREATE TABLE IF NOT EXISTS " + table + "(`ID1` int(11) NOT NULL AUTO_INCREMENT"
        for i in range (1,len(self.fields)):
            query += ", "
            query += "`"+self.fields[i][0]+"` "
            if self.fields[i][1] == 'C':   # Character field
                query += "VARCHAR("+str(self.fields[i][2])+") "
            elif self.fields[i][1] == 'N': # Numeric field
                if self.fields[i][3] == 0:
                    query += "INT "
                else:
                    query += "FLOAT "
            elif self.fields[i][1] == 'D': # Date field
                query += "DATE "
        query += ", `GEOMETRY` "
        if self.points[0].shapeType == 1:
            query += "POINT"
        elif self.points[0].shapeType == 3:
            query += "LINESTRING"
        else:
            query += "POLYGON"
        query += " NOT NULL"
        query += ", PRIMARY KEY(`ID1`), SPATIAL `GEOMETRY`(`GEOMETRY`)"
        query += ") ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;"
        return query
        
    def getFieldNames(self):
        out = []
        for i in range (1,len(self.fields)):
            out.append(self.fields[i][0])
        out.append("GEOMETRY")
        return out
   
    def getShapes(self):
        out = []
        for i in range(0,len(self.points)):
            attributes = collections.OrderedDict()
            for j in range(0,len(self.records[i])):
                if self.fields[j+1][1] == 'C':   # Character field
                    attributes[self.fields[j+1][0]] = self.records[i][j].strip()
                elif self.fields[j+1][1] == 'N': # Numeric field
                    attributes[self.fields[j+1][0]] = self.records[i][j]
                elif self.fields[j+1][1] == 'D': # Date field
                    attributes[self.fields[j+1][0]] = str(datetime.date(self.records[i][j][0],self.records[i][j][1],self.records[i][j][2]))
            if self.points[i].shapeType == 1:
                bbox = self.points[i]
                parts = [self.points[i]]
            else:
                bbox = self.points[i].bbox
                parts = self.points[i].parts
            out.append([self.points[i].shapeType,self.points[i].points,attributes,bbox,parts])
        return out
