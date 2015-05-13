# 
# Open addresses Spatial Research
# OS Open Names ETL Script
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Load OS Open Names
#

import csv
import glob
import MySQLdb
import string
import collections
from bulkinsert import *
import codecs

# Database configuration
username = "****"
password = "****"
hostname = "****"
database = "****"

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database, use_unicode=True, charset='utf8')
cur = dbConn.cursor() 

query = "TRUNCATE TABLE `gaz_opennames`;"
cur.execute(query)

openNames_fields = ['OS_ID','NAMES_URI','NAME1','NAME1_LANG','NAME2','NAME2_LANG','TYPE','LOCAL_TYPE','GEOMETRY_X','GEOMETRY_Y','GEOMETRY','MOST_DETAIL_VIEW_RES','LEAST_DETAIL_VIEW_RES','MBR_XMIN','MBR_YMIN','MBR_XMAX','MBR_YMAX','MBR','POSTCODE_DISTRICT','POSTCODE_DISTRICT_URI','POPULATED_PLACE','POPULATED_PLACE_URI','POPULATED_PLACE_TYPE','DISTRICT_BOROUGH','DISTRICT_BOROUGH_URI','DISTRICT_BOROUGH_TYPE','COUNTY_UNITARY','COUNTY_UNITARY_URI','COUNTY_UNITARY_TYPE','REGION','REGION_URI','COUNTRY','COUNTRY_URI','RELATED_SPATIAL_OBJECT','SAME_AS_DBPEDIA','SAME_AS_GEONAMES']

openNames_bi = BulkInsert(cur,"gaz_opennames",openNames_fields, max=100, ignore=True)

file = "DOC/OS_Open_Names_Header.csv"
  
csvfile = open(file, 'r')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in reader:
    csv_names = [unicode(cell, 'utf-8-sig') for cell in row]
csvfile.close()

print csv_names

nwrit = 0;

for file in sorted(glob.glob("DATA/*.csv")):
    print file
    nrecs = 0
    csvfile = open(file, 'r')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        row = dict(zip(csv_names,[unicode(cell, 'utf-8-sig') for cell in row]))
        nrecs += 1
        # print row
        
        if (nrecs % 10000) == 0:
                print "Records read: " + str(nrecs)
                
        line = []
        
        for field in csv_names:
            # print field
            # print row[field]
            if field[0:4] == u'GEOM' or field[0:3] == u'MBR':
                if row[field] == '':
                    line.extend([u'0'])
                else:
                    line.extend([row[field]])
            else:
                line.extend([row[field]])
            if field == 'GEOMETRY_Y':
                if row[field] == '':
                    line.extend([u"GeomFromText('Point(0 0)')"])
                else:
                    line.extend([u"GeomFromText('Point("+row['GEOMETRY_X']+" "+row['GEOMETRY_Y']+")')"])
            if field == 'MBR_YMAX':
                if row[field] == '':
                    line.extend([u"GeomFromText('Polygon((0 0,0 0,0 0,0 0,0 0))')"])
                else:
                    line.extend([u"GeomFromText('Polygon(("+row['MBR_XMIN']+" "+row['MBR_YMIN']+","+row['MBR_XMIN']+" "+row['MBR_YMAX']+","+row['MBR_XMAX']+" "+row['MBR_YMAX']+","+row['MBR_XMAX']+" "+row['MBR_YMIN']+","+row['MBR_XMIN']+" "+row['MBR_YMIN']+"))')"])

        # print line    
        openNames_bi.addRow(line)
        nwrit += 1
            
    print "Records read: " + str(nrecs) + " Written: " + str(nwrit)

    csvfile.close()
 
openNames_bi.close() 
dbConn.commit()
print "Writing changes to database"
dbConn.close()
