import math
import numpy
import sys, os
import xml.etree.ElementTree as ET


Re = 6371000  # Earth radius in meters

# Extract the latitute and longitude as a tuple in radians from a <trkpt> element
def extract(trkpt) :
	return (math.pi / 180 * float(trkpt.attrib['lat']), math.pi / 180 * float(trkpt.attrib['lon']))

# Compute the great circle distance between two points given in polar
# coordinates and radians. The return value is in the same units as
# Re is defined.
def dist(p0, p1) :
	a = math.sin((p1[0] - p0[0])/2)**2 + math.cos(p0[0]) * math.cos(p1[0]) * math.sin((p1[1] - p0[1])/2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	return Re * c

# Convert from polar to cartesian coordinates, radians to units of Re
def polcar(polarpt) :
	lat,lon = polarpt
	# Quick sanity check
	assert lat > -2*math.pi and lat < 2*math.pi
	assert lon > -2*math.pi and lon < 2*math.pi
	xyz = (math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))
	return Re * numpy.array(xyz)

# Convert from cartesian to polar coordinates, radians to units of Re
def carpol(xyz) :
	R = numpy.linalg.norm(xyz)
	# Quick sanity check
	assert (R-Re)*1.0/Re < 1e-14

	lat = math.asin(numpy.dot(numpy.array([0,0,1]), xyz) / R)

	xy = xyz.copy()
	xy[2] = 0
	xy /= numpy.linalg.norm(xy)
	lon = math.atan2(xy[1], xy[0])

	return numpy.array( (lat,lon) )

# Given a pair of polar coordinates and a third, find the shortest great circle
# distance from the third point to the great circle arc segment connecting
# the first two.
def greatcircle_point_distance(pair, third) :
	# Convert to cartesian coordinates for the vector math
	cpair = tuple( map(lambda pt: polcar(numpy.array(pt)), pair) )
	cthird = polcar(numpy.array(third))

	# Project 'third' onto the great circle arc joining 'pair' along the
	# vector that is normal to the chord between 'pair'
	normal = numpy.cross(*cpair)
	normal /= numpy.linalg.norm(normal)
	intersect = cthird - normal * numpy.dot(normal, cthird)
	intersect *= Re / numpy.linalg.norm(intersect)

	# Great circle distance from 'third' to its projection
	d = dist(third, carpol(intersect))

	# If the projection of 'third' is not between the shorter arc
	# connecting 'pair', we instead want the gc distance from 'third'
	# to the nearest of the two.
	d0 = numpy.dot(intersect, cpair[0])
	d1 = numpy.dot(intersect, cpair[1])
	c = numpy.dot(numpy.cross(intersect, cpair[0]), numpy.cross(intersect, cpair[1]))

	if c < 0 and ((d0 >= 0 and d1 >= 0) or  (d0 < 0 and d1 < 0)) :
		return d
	else :
		return min((dist(third, pair[0]), dist(third, pair[1])))

# Examine a segment of gpx track and set 'keep' attributes on points
# as needed to stay within maxdistance and maxinterval.
#
# Given two kept trackpoints with no other kept points between them, the
# distance between the arc connecting these two points and any other
# trackpoints between them must be less than 'maxdistance'.
#
# Given two kept trackpoints, the distance between them should not be
# significantly greater than 'maxinterval'.
def process(seg, maxdistance = 5, maxinterval = 10) :
	bnds = (extract(seg[0]), extract(seg[-1]))

	# Find the point between this segment's endpoints that lies furthest
	# from the great circle arc between these endpoints
	idx,maxd = None,None
	for n in range(1, len(seg) - 1) :
		this = extract(seg[n])
		d = greatcircle_point_distance(bnds, this)
		if maxd is None or d > maxd :
			maxd = d
			idx = n

	if maxd > maxdistance :
		# Keep this point if it is at least 'maxdistance' from the
		# connecting arc, and run 'process' on the two subsegments
		seg[idx].attrib['keep'] = 'True'
		process(seg[:idx], maxdistance, maxinterval)
		process(seg[idx:], maxdistance, maxinterval)
	elif maxinterval > 0 :
		# This segment is good enough in terms of direction of travel.
		# A maximum distance between points may also be desired, however,
		# so loop through all remaining discarded points and add as needed.
		prev = bnds[0]
		fin = bnds[1]
		for pt in seg :
			this = extract(pt)
			if dist(prev, this) > maxinterval and dist(fin, this) > maxinterval :
				# Note that this does not satisfy the 'maxinterval' limit,
				# but instead takes the next point just further than the
				# given limit.
				# FIXME might be better to take the previous point, to make
				# the limit a guaranteed one.
				pt.attrib['keep'] = 'True'
				prev = this

	return seg

if __name__ == "__main__" :

	if len(sys.argv) < 4 :
		print ("Usage: %s <gpx file> <maximum distance> <maximum interval>"%sys.argv[0])
		sys.exit(-1)

	file = os.path.splitext(sys.argv[1])
	assert file[1] == '.gpx' or file[1] == ''
	maxdistance = int(sys.argv[2])
	maxinterval = int(sys.argv[3])

	with open(file[0] + '.gpx', 'r') as fh :
		root = ET.parse(fh).getroot()
		NS = "{" + root.nsmap[None] + "}"

	# <gpx> contains a <trk> element, which contains a <trkseg> element
	# FIXME rewrite this to iterate over tracks and segments
	trkseg = root.find(NS + "trk").find(NS + "trkseg")

	# Add a 'keep' attribute to each <trkpt> element in the <trkseg>
	# Also remove elevation data
	print ("Note: this script will also strip elevation data, assuming it to be inaccurate")
	for pt in trkseg :
		pt.attrib['keep'] = "False"
		for e in pt.iter(NS + "ele") :
			pt.remove(e)

	# We assume we need the first and last point
	# TODO make this configurable, to allow processing of only
	#      part of a track
	trkseg[0].attrib['keep'] = 'True'
	trkseg[-1].attrib['keep'] = 'True'

	process(trkseg, maxdistance, maxinterval)

	# Remove the unneeded trackpoints based on the 'keep' attribute
	m = len(trkseg)
	kill = filter(lambda pt: pt.attrib['keep'] == 'False', trkseg)
	for n in range(0, len(kill)) :
		trkseg.remove(kill[n])
	n = len(trkseg)
	print ("%d -> %d"%(m,n))

	# Remove the 'keep' attribute
	for n in range(0, len(trkseg)) :
		trkseg[n].attrib.pop('keep')

	# Write out the modified GPX file
	fh = open(file[0] + '_mod.gpx', 'w')
	xml = fh.write(ET.tostring(root, pretty_print=True, xml_declaration=True))
	fh.close()
