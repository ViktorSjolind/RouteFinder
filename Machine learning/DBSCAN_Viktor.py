# -*- coding: utf-8 -*-
"""
Based upon the official scikit example,
the goal is to load a .csv file and find clusters

Todo:
-fix eps and min_sample values
-confirm a single trip doesn't make a cluster

Created on Sat Dec 15 19:16:24 2018

@author: Viktor
"""

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import folium
import pandas as pd
import numpy as np
from random import randint


def drawPointsOnMap(superMap, points, color, radiusSize):
    for point in points:        
        folium.CircleMarker((point), radius = int(radiusSize), fill=True, fill_color = color, color = color, fill_opacity=0.6).add_to(superMap)
        folium.CircleMarker((point), radius = 2, fill=True, fill_color = "ff000000", color = "ff000000", fill_opacity=1).add_to(superMap)
    
# Take the average for each X coordinates    
def reducePoints(points):
    points = sorted(points, key=lambda x: x[0])
    dividor = 9
    newPoints = []
    index = 0
    pointSumX = 0
    pointSumY = 0
    for point in points:
        pointSumX += point[0]
        pointSumY += point[1]
        if index%dividor==0:
            subArray = [pointSumX / dividor, pointSumY / dividor]
            newPoints.append(subArray)
            pointSumX = 0
            pointSumY = 0
        index+=1
    return newPoints
        
# DataFrame with all coordinates
# Map points are just arrays inside arrays
df = pd.read_csv("DataFrame.csv", index_col = False, header=0)

# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(df.values)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)




print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

# Plot result
superMap = folium.Map(location=[60.19265, 21.914834], zoom_start=20, tiles='OpenStreetMap')
unique_labels = set(labels)
for k in unique_labels:
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)
    xy = df.values[class_member_mask & core_samples_mask]   
    
    color = '#{:06x}'.format(randint(0, 256**3))
    drawPointsOnMap(superMap, xy, color, 20)
    
newPoints = reducePoints(df.values)
color = '#{:06x}'.format(randint(0, 256**3))
drawPointsOnMap(superMap, newPoints, color, 20)
    
superMap.save('map-viktor.html')
print("All done")