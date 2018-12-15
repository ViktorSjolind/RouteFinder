'''
Creates a DataFrame of a .gpx file

input: path to the directory that contains .gpx files
output: dataframe containing all the trips, with coordinates,
depth and local time.
'''

from xml.dom import minidom
import os
import pandas as pd

def parse_xml(path):
    id=0
    trips = []
    for filename in os.listdir(path):
        if not filename.endswith('.gpx'): continue
        fullname = os.path.join(path, filename)
        gpx_file = open(fullname, 'r')
        xmldoc = minidom.parse(gpx_file)
        gpx = xmldoc.getElementsByTagName("gpx")[0]
        id = id+1 # Keeps count of the trips.

        # Get the coordinate points and depth.
        trk = gpx.getElementsByTagName("trk")[0]
        trkseg =trk.getElementsByTagName("trkseg")[0]
        trkpts = trkseg.getElementsByTagName("trkpt")

        # For each coordinate point, append it to the trip list.
        for trkpt in trkpts:
            #trips.append((trkpt.getAttribute("lat"), trkpt.getAttribute("lon"),trkpt.getAttribute("dpt"), "Trip: {}".format(id),))
            trips.append((trkpt.getAttribute("lat"), trkpt.getAttribute("lon")))
    # Convert the trip list into a dataframe.
    #df = pd.DataFrame(trips, columns=['Longitude', 'Latitude','Depth','TripNo'])
    df = pd.DataFrame(trips, columns=['Longitude', 'Latitude'])
    return df
