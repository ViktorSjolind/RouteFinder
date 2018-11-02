import xml.etree.ElementTree as ET
import random

tree = ET.parse('trip_official.gpx')
root = tree.getroot()

#To get same format as original GPX file
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace("", "http://www.topografix.com/GPX/1/1")


for x in range(10):
    #List of attributes
    lonsim = []
    latsim = []
    dptsim = []
    
    #Dirty for-loop mmhmmhmhm
    for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
        for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
            for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
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



    #Offset coordinates
    #Implement random variable somehow
    #Test if random.uniform works, does the coordinates vary too much?

    a = 0
    for y in f_lonsim:
        #y = round((y + random.uniform(0.000001, 0.000003)),6) OG code
        y = round((y + random.uniform(-0.0003, 0.0003)), 6)
        f_lonsim[a] = y
        a = a + 1
        
    b = 0
    for z in f_latsim:
        #z = round((z + random.uniform(0.000001, 0.000003)),6) OG code
        z = round((z + random.uniform(-0.0003, 0.0003)), 6)
        f_latsim[b] = z
        b = b + 1
        #print (z)

    #Convert lists back to string format so we can write them to GPX file
    s_lonsim = [str (x) for x in f_lonsim]
    s_latsim = [str (x) for x in f_latsim]
    s_dptsim = [str (x) for x in f_dptsim]


    i = 0; #Variable for coordinate offset iteration

    for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
        for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
            for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
                trkpt.attrib['lon'] = s_lonsim[i] # Changes the value of longitude attribute
                trkpt.attrib['lat'] = s_latsim[i] # Changes the value of longitude attribute
                i = i + 1
                
                
    tree.write('trip_unofficial_'+str(x)+'.gpx')

