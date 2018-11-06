from xml.dom import minidom
import os 

'''
input: path to the directory that contains .gpx files
output: 3 dimensional array containing all trips with all their 
        respective coordinates and depth
'''
def parse_xml(path):
    id=0
    trips = []
    for filename in os.listdir(path):
        if not filename.endswith('.gpx'): continue
        fullname = os.path.join(path, filename)
        gpx_file = open(fullname, 'r')
        xmldoc = minidom.parse(gpx_file)
        gpx = xmldoc.getElementsByTagName("gpx")[0]
        id = id+1 # Count each trip

        # Get the gps data and depth
        trk = gpx.getElementsByTagName("trk")[0]
        trkseg =trk.getElementsByTagName("trkseg")[0]
        trkpts = trkseg.getElementsByTagName("trkpt")

        trip = []
        # For each coordinate point, append it to the trip list
        for trkpt in trkpts:
            trip_data = []
            trip_data.append(id)
            trip_data.append(trkpt.getAttribute("lat"))
            trip_data.append(trkpt.getAttribute("lon"))
            trip_data.append(trkpt.getAttribute("dpt"))

            print("Trip: {}".format(id),
                trkpt.getAttribute("lat"),
                trkpt.getAttribute("lon"),
                trkpt.getAttribute("dpt"),
            )

            trip.append(trip_data)
        # When all coordinate points have been looped through and
        # added to the trip list, add the trip to the list of all trips.
        trips.append(trip)
    return trips
