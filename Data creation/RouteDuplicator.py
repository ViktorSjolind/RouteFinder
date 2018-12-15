"""
Module for duplicating routes with an offset
"""

import xml.etree.ElementTree as ET
import random

# To get same format as original GPX file
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace("", "http://www.topografix.com/GPX/1/1")


#iterations = number of routes to create
#routeName = the file that the routes should be based on
def Duplicate(iterations, routeName):    
    for iteration in range(iterations):
    
        tree = ET.parse(routeName)
        root = tree.getroot()
    
        # List of attributes
        lonsim = []
        latsim = []
        dptsim = []
    
        # Dirty for-loop mmhmmhmhm
        for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
            for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
                for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
                    lonsim.append(trkpt.attrib["lon"])
                    latsim.append(trkpt.attrib["lat"])
                    dptsim.append(trkpt.attrib["dpt"])
                    # lonsim and latsim lists full of same coordinates, check for iteration error?
    
                    # trkpt.attrib["dpt"] = "test" # Changes the value of 'dpt' attribute
                    # print (trkpt.attrib)
    
        # Convert lists to float values so we can offset them
        f_lonsim = [float(iteration) for iteration in lonsim]
        f_latsim = [float(iteration) for iteration in latsim]
        f_dptsim = [float(iteration) for iteration in dptsim]
    
        # Offset coordinates
        # Test if random.uniform works, do the coordinates vary too much?
    
        a = 0
        for y in f_lonsim:
            # y = round((y + random.uniform(0.000001, 0.000003)),6) OG code
            # y = round((y + random.uniform(-0.0001, 0.0001)), 6)
    
            # Create random variables for offsetting
            even_round = random.uniform(0, 0.0002)
            odd_round = random.uniform(-0.0002, 0)
    
            # Offset based on if number_of_iterations is even or odd
            if (iteration % 2) == 0:
                y = round((y + even_round), 6)
                f_lonsim[a] = y
                a = a + 1
            else:
                y = round((y + odd_round), 6)
                f_lonsim[a] = y
                a = a + 1
    
        b = 0
        for z in f_latsim:
            # z = round((z + random.uniform(0.000001, 0.000003)),6) OG code
            # z = round((z + random.uniform(-0.0001, 0.0001)), 6)
    
            # Create random variables for offsetting
            even_round = random.uniform(0, 0.0002)
            odd_round = random.uniform(-0.0002, 0)
    
            # Offset based on if number_of_iterations is even or odd
            if (iteration % 2) == 0:
                z = round((z + even_round), 6)
                f_latsim[b] = z
                b = b + 1
            else:
                z = round((z + odd_round), 6)
                f_latsim[b] = z
                b = b + 1
    
        # Convert lists back to string format so we can write them to GPX file
        s_lonsim = [str(iteration) for iteration in f_lonsim]
        s_latsim = [str(iteration) for iteration in f_latsim]
        s_dptsim = [str(iteration) for iteration in f_dptsim]
    
        i = 0;  # Variable for coordinate offset iteration
    
        for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
            for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
                for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
                    trkpt.attrib['lon'] = s_lonsim[i]  # Changes the value of longitude attribute
                    trkpt.attrib['lat'] = s_latsim[i]  # Changes the value of longitude attribute
                    i = i + 1
    
        iteration += 1
        tree.write(routeName.replace(".gpx",str(iteration) + '.gpx'))
    
    #What is this line doing? 
    #mplleaflet.show()