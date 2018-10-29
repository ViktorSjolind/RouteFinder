from xml.dom import minidom
import os 
lat = []
lon = []
depth= []
LocTime = []
id=0
path = "C:/Users/Ashenafi/Desktop/ProjectWork/xml_files"
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
        lat.append(trkpt.getAttribute("lat"))
        lon.append(trkpt.getAttribute("lon"))
        depth.append(trkpt.getAttribute("dpt"))
        LocTime.append(trkpt.getAttribute("time"))
        print("Trip: {}".format(id),trkpt.getAttribute("lat"),trkpt.getAttribute("lon"),trkpt.getAttribute("dpt") )
