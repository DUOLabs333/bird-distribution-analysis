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
    

birds_locations=collections.defaultdict(lambda : [])
locations=[]
location_num=0

#Parse each kml file to extract the coordinate boxes for the squares, and what birds were in each box
import xml.etree.ElementTree as ET
for file in ["north","southeast","west"]:
    tree = ET.parse(f'bba{file}.kml')
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    for location in tree.iterfind(".//kml:Placemark",namespaces):
        coordinates=location.find(".//kml:LinearRing/kml:coordinates",namespaces).text.strip()
        coordinates=coordinates.split(" ")
        coordinates=[_.split(",")[:-1] for _ in coordinates]
        coordinates=[[float(_) for _ in coor] for coor in coordinates] #Parse out the coordinates for each survey square used
        fromproj=pyproj.crs.CRS(4326)
        toproj=pyproj.crs.CRS(32632)
        transformer=pyproj.Transformer.from_crs(fromproj,toproj,always_xy=True)
        locations.append(shapely.ops.transform(transformer.transform,shapely.geometry.Polygon(coordinates)))
        for bird in location.iterfind(".//kml:SimpleData",namespaces):
            if not bird.text.isspace() and bird.text!='NONE': #Only add a park as a location where the bird is found if the bird has been found at that location
                birds_locations[bird.text].append(location_num)
        location_num+=1


parks_total_area=sum(park.area for park in shapely.ops.unary_union(parks).geoms)
with shapefile.Reader("State.shp") as reader:
    fromproj=pyproj.crs.CRS(open("State.prj").read())
    toproj=pyproj.crs.CRS(32632)
    transformer=pyproj.Transformer.from_crs(fromproj,toproj,always_xy=True)
    
    state_area=shapely.ops.transform(transformer.transform,shapely.geometry.Polygon(reader.shape(0).points)).area-parks_total_area


birds_ratios={}


import shapely.strtree

parks_tree=shapely.strtree.STRtree(parks)

import pdb
for bird in birds_locations:
    inside=0
    outside=0
    for location in birds_locations[bird]:
        location_area=locations[location].area
        park=shapely.ops.unary_union(parks_tree.query(locations[location]))
        intersection=park.intersection(locations[location]).area
        if abs(intersection)<10**(-7):
            intersection=0
            
        if (intersection>location_area-intersection):
            inside+=location_area
        else:
            outside+=location_area

    if outside==0:
        birds_ratios[bird]="Infinity"
    else:
        birds_ratios[bird]=(inside/parks_total_area)/(outside/state_area)
        if birds_ratios[bird]<10**(-4):
            birds_ratios[bird]=0

import csv

with open("analysis_results.csv","w+") as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(["Bird","Ratio"])
    for bird in birds_ratios:
        writer.writerow([bird,birds_ratios[bird]])
