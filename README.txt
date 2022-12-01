To get started:
1. Install the geos library for your platform

2. Download the bird data
wget http://www.dec.ny.gov/maps/bba{southeast,west,north}.kmz
unzip '*.kmz'
rm *.kmz

3. Download the state parks data
wget http://gis.ny.gov/gisdata/data/ds_1114/DEC_lands.zip
unzip DEC_lands.zip DecLands.{shp,dbf,prj}
rm DEC_lands.zip

4. Download the state borders data
wget "https://gis.ny.gov/gisdata/fileserver/?DSID=927&file=NYS_Civil_Boundaries.shp.zip" -O NYS_Civil_Boundaries.shp.zip
unzip NYS_Civil_Boundaries.shp.zip Shape.{dbf,shp,prj}
rm NYS_Civil_Boundaries.shp.zip

5. Run the scripts
python analysis.py && python get_habitats.py && python compare.py
