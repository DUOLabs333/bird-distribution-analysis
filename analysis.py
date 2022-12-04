import sys,os,collections,math
os.chdir(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0,"_vendor")

import shapefile,pyproj,shapely.geometry,shapely.ops

parks=[]

#Find boundaries to all state parks
with shapefile.Reader("DecLands.shp") as reader:
    fromproj=pyproj.crs.CRS(open("DecLands.prj").read())
    toproj=pyproj.crs.CRS(32632)
    transformer=pyproj.Transformer.from_crs(fromproj,toproj,always_xy=True)
    for shape in reader.shapes():
        #parks.append(shapely.ops.transform(transformer.transform,shapely.geometry.box(*shape.bbox)))
        parks.append(shapely.ops.transform(transformer.transform,shapely.geometry.Polygon(shape.points).convex_hull)) #Use convex hull to avoid self-intersections
    

locations=[]
#Parse each kml file to extract the coordinate boxes for the squares, and what birds were in each box

import shapely.strtree

parks_tree=shapely.strtree.STRtree(parks)

import xml.etree.ElementTree as ET
import csv
csvfile=open("analysis_results.csv","w+")
writer=csv.writer(csvfile)
writer.writerow(["Location","Birds","Prefer Forests?"])
location_num=0
for file in ["north","southeast","west"]:
    tree = ET.parse(f'bba{file}.kml')
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    for location in tree.iterfind(".//kml:Placemark",namespaces):
        row=[location_num,[],0]
        
        coordinates=location.find(".//kml:LinearRing/kml:coordinates",namespaces).text.strip()
        coordinates=coordinates.split(" ")
        coordinates=[_.split(",")[:-1] for _ in coordinates]
        coordinates=[[float(_) for _ in coor] for coor in coordinates] #Parse out the coordinates for each survey square used
        fromproj=pyproj.crs.CRS(4326)
        toproj=pyproj.crs.CRS(32632)
        transformer=pyproj.Transformer.from_crs(fromproj,toproj,always_xy=True)
        polygon=shapely.ops.transform(transformer.transform,shapely.geometry.Polygon(coordinates))
        for bird in location.iterfind(".//kml:SimpleData",namespaces):
            if not bird.text.isspace() and bird.text!='NONE': #Only add a park as a location where the bird is found if the bird has been found at that location
                row[1].append(bird.text)
                
        park=shapely.ops.unary_union(parks_tree.query(polygon))
        intersection=park.intersection(polygon).area
        row[2]=int(intersection>polygon.area-intersection) #If more of the location intersected with parks, then it can be considered a forested area
        writer.writerow(row)
