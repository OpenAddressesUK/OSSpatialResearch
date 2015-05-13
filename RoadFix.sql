-- Create correction lookup for missing formsPart fields in OS OpenRoads
CREATE TABLE `roadlink_fix` 
SELECT spa_roadlink.identifier,gaz_opennames.OS_ID 
FROM gaz_opennames 
INNER JOIN spa_roadlink ON gaz_opennames.NAME1 = spa_roadlink.name1 
WHERE spa_roadlink.formsPart = '' AND gaz_opennames.OS_ID LIKE 'osgb%' AND ST_INTERSECTS(spa_roadlink.GEOMETRY,gaz_opennames.MBR)
