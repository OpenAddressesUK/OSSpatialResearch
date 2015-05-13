# 
# Open addresses ETL Common Library
# Open addresses Extract Point From Point Collection Shapefile
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Extract points and attributes from shapefile
#

import shapefile
import datetime
import glob
import sys
import collections
from pprint import pprint
from extract_shape import *
from bulkinsert import *
import os.path
import fnmatch
import os

tol = 5                                 # Tolerance

if len(sys.argv) > 2:
    print "Invalid arguments. Usage is 'python shapetest.py [directory]'"
    sys.exit()
elif len(sys.argv) == 2:
    folder = sys.argv[1]
else:
    folder = "."
    
# Read database configuration from config file
username = "****"
password = "*******"
hostname = "*******"
database = "****"

tables = {}
shape_bi = {}
shape_fields = {}

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
cur = dbConn.cursor() 

dbConn.set_character_set('utf8')
cur.execute('SET NAMES utf8;') 
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

nfiles = 0
nrecs = 0
nupdate = 0

matches = []
for root, dirnames, filenames in os.walk('./'):
  for filename in fnmatch.filter(filenames, '*.shp'):
    matches.append(os.path.join(root, filename))
    # print "root="+root
    # print "filename="+filename

# for file in glob.glob(folder+"/data/*.shp"):

for file in sorted(matches):
    base = os.path.basename(file).split('.')[0].lower()
    prefix = base.find('_')
    if prefix > -1:
        base = base[prefix+1:]
    base = "oml_" + base
    print base
    print "File: "+file+" Base: "+base
    sf = shapeExtract(file)
    if base not in tables:
        query = "DROP TABLE IF EXISTS `"+base+"`;"
        cur.execute(query)
        query = sf.getTableSQL(base)
        cur.execute(query)
        shape_fields[base] = sf.getFieldNames()
        # print shape_fields
        shape_bi[base] = BulkInsert(cur,base,shape_fields[base],max=100)
        tables[base] = 0

    tables[base] += 1
    for shape in sf.getShapes():
        params = []
        for i in range(0,len(shape_fields[base])-1):
            params.append(shape[2][shape_fields[base][i]])
        # print shape[4]
        if shape[0] == 1:
            # print shape
            geom = "GeomFromText('POINT("+str(shape[1][0][0]) + " " + str(shape[1][0][1])+")')"
        else:
            if shape[0] == 3:
                geom = "GeomFromText('LINESTRING("
                for i in range(0,len(shape[1])):
                    if i > 0:
                        geom += ","
                    geom += str(shape[1][i][0]) + " " + str(shape[1][i][1])
                geom += ")')"
            else:
                geom = "GeomFromText('POLYGON("
                shape[4].extend([len(shape[1])])
                for i in range(1,len(shape[4])):
                    if i > 1:
                        geom += ","
                    geom += "("
                    for j in range(shape[4][i-1],shape[4][i]):
                        if j > shape[4][i-1]:
                            geom += ","
                        geom += str(shape[1][j][0]) + " " + str(shape[1][j][1])
                    geom += ")"
                geom += ")')"
        # print geom
        params.append(geom)
        #print params
        shape_bi[base].addRow(params)
        nrecs += 1
        if nrecs % 1000 == 0:
            print "Records read: " + str(nrecs)
            
    dbConn.commit()
            
print "Records read: " + str(nrecs)

if nfiles > 0:
    for table in shape_bi:
        shape_bi[table].close()

dbConn.commit()
dbConn.close()
