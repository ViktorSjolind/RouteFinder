# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:57:06 2018

@author: Ashenafi
"""

from xml.dom import minidom
import os 
import pandas as pd
from pandas import DataFrame
lat = []
lon = []
depth= []

List_for_all = []

path = "C:/Users/Ashenafi/Desktop/ProjectWork/xml_files"
def XMLParser(path):
    id=0
    for filename in os.listdir(path):
        if not filename.endswith('.gpx'): continue
        fullname = os.path.join(path, filename)
        gpx_file = open(fullname, 'r')
        xmldoc = minidom.parse(gpx_file)
        gpx = xmldoc.getElementsByTagName("gpx")[0]
        id = id+1 # counts each trips
    #get the gps,depth, Local time
        trk = gpx.getElementsByTagName("trk")[0]
        trkseg =trk.getElementsByTagName("trkseg")[0]
        trkpts = trkseg.getElementsByTagName("trkpt")
    
        for trkpt in trkpts:
            List_for_all.append(("Trip: {}".format(id),trkpt.getAttribute("lat"), trkpt.getAttribute("lon"),trkpt.getAttribute("dpt")) )
            
XMLParser(path)

df = DataFrame(List_for_all, columns=['TripNo','Longitude', 'Latitude', 'Depth'])   
print(df.shape) #the size of the dataframe
print(df.head()) #the first five
print(df.tail()) #the last five
print (df.loc[df['TripNo'] == 'Trip: 2'] ) # only trip 2
df.to_csv('outputascsv_1.csv') # save the data as csv file
