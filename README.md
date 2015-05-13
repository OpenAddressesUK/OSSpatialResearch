OSSpatialResearch
=================
This is the repository for Open Addresses' "Spatial Research" Python scripts, data files and SQL used during our evaluation of Ordnance Survey Open Map and Open Roads , part of the solution we deployed for to ascertain their potential to improve the accuracy of our services.

## Dependencies

The Python scripts require the external PyShp shapefile Python library. Consult the installation guide for your OS for instructions.

They also require the common bulkinsert.py and extract_shape.py scripts included in this repository.

## Running

### Clone this repo:

    git clone git@github.com:OpenAddressesUK/OSSpatialResearch.git

### Create a database

Create a MySQL, or compatible RDBMS, database with spatial support and default character set utf8-unicode

Create a user on the database with admin rights to create, delete and truncate tables.

Amend the Python scripts to add the server, user, password and database name parameters. 

### Populate the database

Download the latest version of OS Open Map Local and OS Open Roads from the [Ordnance Survey Open Data Portal](http://www.ordnancesurvey.co.uk/business-and-government/products/opendata-products-grid.html)

Unzip both files

To load OS Open Map, run the command

    python load_OpenMap.py *directory*
    
If directory is ommitted, the script will run in the current directory.

The script will recurse the directory structure and aggregate the Os grid tiles, creating one table per shapefle type in Open Map with the Geometry field appended.

### Fix missing data

Run the RoadFx.sql script on the database after it is loaded.

This will create a look up table from which the missing components in Open Roads can be added.

### Test the database

To test the database, run the Python script getAddrFromOS.py:

        python getAddrFromOS.py *postcode* *maxdist*
        
Where

        *postcode* is the postcode to be search without any spaces
        *maxdist* is the maximum distance from the postcode centroid to search for address components

## Licence
This code is open source under the MIT license. See the [LICENSE.md](LICENSE.md) file for full details.

