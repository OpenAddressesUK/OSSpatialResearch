# 
# Open addresses Spatial Research
# Display Candidate Address Components From OS Open Map & Open Roads
#
#
# Version       1.0 (Python) in progress
# Author        John Murray
# Licence       MIT
#
# Purpose       Display Candidate Address Components
#

import MySQLdb
import collections
import sys
    
# Database configuration
username = "****"
password = "********"
hostname = "********"
database = "****"

if len(sys.argv) != 3:
    print "Invalid arguments. Usage is 'python getAddrFromOS.py postcode buffer'"
    sys.exit()
else:
    postcode = sys.argv[1]
    buf_size = int(sys.argv[2])

dbConn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
cur = dbConn.cursor() 

query = "SELECT `name1`,`formOfWay`,`length`,`formsPart`,ST_DISTANCE(`GEOMETRY`,(SELECT `GEOMETRY`FROM `gaz_opennames` WHERE `OS_ID` = '"+postcode+"')) AS `Distance` FROM `spa_roadlink` WHERE `ID` IN (SELECT `ID` FROM `spa_roadlink` WHERE ST_INTERSECTS(`GEOMETRY`,(SELECT ST_BUFFER(`GEOMETRY`,"+str(buf_size)+") FROM `gaz_opennames` WHERE `OS_ID` = '"+postcode+"'))) ORDER BY `Distance`"

print query 

cur.execute(query)
data = cur.fetchall()

streets = []

for d in data:
    if d[3] != '':
        for s in d[3].split(","):
            query = "SELECT `NAME1`, `TYPE`, `LOCAL_TYPE`, `POSTCODE_DISTRICT`, `POPULATED_PLACE`, `DISTRICT_BOROUGH`, `COUNTY_UNITARY`, `REGION`, `COUNTRY`, `RELATED_SPATIAL_OBJECT` FROM `gaz_opennames` WHERE `OS_ID` = '"+s+"'"
            cur.execute(query)
            for d1 in cur.fetchall():
                if d1[0] not in streets:
                    print "Street: "+d1[0]
                    print "Settlement: "+d1[4]
                    print "Postcode: "+postcode[0:-3]+" "+postcode[-3:]
                    print "County: "+d1[6]
                    print "Distance: "+str(d[4])
                    print
                    streets.extend([d1[0]])

