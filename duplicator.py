import xml.etree.ElementTree as ET
import random

tree = ET.parse('simtrip1.gpx')
root = tree.getroot()

#List of attributes
lonsim = []
latsim = []
dptsim = []


#Dirty for-loop mmhmmhmhm
for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
    for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
        for trkpt in trkseg.iter('{http://www.topografix.com/GPX/1/1}trkpt'):
            lonsim.append (trkpt.attrib["lon"])
            latsim.append (trkpt.attrib["lat"])
            dptsim.append (trkpt.attrib["dpt"])
            #lonsim and latsim lists full of same coordinates, check for iteration error?
            
            #trkpt.attrib["dpt"] = "test" # Changes the value of 'dpt' attribute
            #print (trkpt.attrib)

#Convert lists to float values so we can offset them
f_lonsim = [float (x) for x in lonsim]
f_latsim = [float (x) for x in latsim]
f_dptsim = [float (x) for x in dptsim]


#offset coordinates
#implement random variable somehow
#test if random.uniform works, does the coordinates vary too much?

for y in f_lonsim:
    y = round ((y + random.uniform(0.000001, 0.000003)),6)
    #print (y)

for z in f_latsim:
    z = round ((z + random.uniform(0.000001, 0.000003)),6)
    #print (z)

#Convert lists back to string format so we can write them to GPX file
s_lonsim = [str (x) for x in lonsim]
s_latsim = [str (x) for x in latsim]
s_dptsim = [str (x) for x in dptsim]

for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
    for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
        for trkpt in trkseg.iter('{http://www.topografix.com/GPX/1/1}trkpt'):
            i = 1;
            trkpt.attrib['lon'] = 'kek'  #s_lonsim[i] # Changes the value of longitude attribute
            trkpt.attrib['lat'] = 'va' #s_latsim[i] # Changes the value of longitude attribute
            i = i + 1
            
tree.write('simtrip1.gpx')
