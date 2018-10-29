from xml.dom import minidom
gpx_file = open('trip_3001650010_995f2029-3509-4950-b318-151a6bba4952', 'r')
xmldoc = minidom.parse(gpx_file)
gpx = xmldoc.getElementsByTagName('gpx')[0]
trk = gpx.getElementsByTagName('trk')[0]
trkseg = gpx.getElementsByTagName('trkseg')[0]
trkpts = gpx.getElementsByTagName('trkpt')
lat = []
lon = []
depth = []
LocTime = []

for trkpt in trkpts:
    lat.append(trkpt.getAttribute('lat'))
    lon.append(trkpt.getAttribute('lon'))
    depth.append(trkpt.getAttribute('dpt'))
    LocTime.append(trkpt.getAttribute('time'))


