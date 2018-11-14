# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:57:17 2018

@author: Ashenafi

"""

import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
#%matplotlib inline


# define the number of kilometers in one radian
kms_per_radian = 6371.0088

# load the data set
df = pd.read_csv('outputascsv_1.csv', encoding='utf-8')
print("#"*30, "print orginal df")
print(df.head())
print("Lenght of the orginal data frame",len(df))

# represent points consistently as (lat, lon)
coords = df.as_matrix(columns=['Longitude', 'Latitude'])

# define epsilon as 1.5 kilometers, converted to radians for use by haversine
epsilon = 0.5 / kms_per_radian

#print (coords)

start_time = time.time()
db = DBSCAN(eps=epsilon, min_samples=5, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_

# get the number of clusters
num_clusters = len(set(cluster_labels))

# all done, print the outcome
message = 'Clustered {:,} points down to {:,} clusters, for {:.1f}% compression in {:,.2f} seconds'
print(message.format(len(df), num_clusters, 100*(1 - float(num_clusters) / len(df)), time.time()-start_time))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(coords, cluster_labels)))


# turn the clusters in to a pandas series, where each element is a cluster of points
clusters = pd.Series([coords[cluster_labels==n] for n in range(num_clusters)])
print (len(clusters))

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

centermost_points = clusters.map(get_centermost_point)


# unzip the list of centermost points (lat, lon) tuples into separate lat and lon lists
lats, lons = zip(*centermost_points)


## from these lats/lons create a new df of one representative point for each cluster

rep_points = pd.DataFrame({'Longitude':lons, 'Latitude':lats})
print ('#'*30 + "rep points")
print(rep_points)


rs = pd.merge(df,rep_points, on=['Latitude','Longitude'] , how= 'left')
print("#"*40 + ' rep points with other oginal data info')
#print(rs)
#df.where(df1.values==df2.values)
#res_points.



# pull row from original data set where lat/lon match the lat/lon of each row of representative points
# that way we get the full details like city, country, and date from the original dataframe
#rs = rep_points.apply(lambda row: df[(df['Latitude']== row['Latitude']) & (df['Longitude']== row['Longitude'])].iloc[:300], axis=1)

print(rs.tail(20))

#(df["Longitude"] != rep_points["Longitude"]).any(1)


# plot the final reduced set of coordinate points vs the original full set
fig, ax = plt.subplots(figsize=[10,6 ])
rs_scatter = ax.scatter(rs['Longitude'], rs['Latitude'], c='#99cc99', edgecolor='None', alpha=0.7, s=120)
df_scatter = ax.scatter(df['Longitude'], df['Latitude'], c='k', alpha=0.9, s=3)
ax.set_title('Full data set vs DBSCAN reduced set')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_xlim([60, 62])
ax.set_ylim([20, 24])
ax.legend([df_scatter, rs_scatter], ['Full set', 'Reduced set'], loc='upper right')
plt.show()


















#import pandas as pd, numpy as np, matplotlib.pyplot as plt
#from sklearn.cluster import DBSCAN
#from geopy.distance import great_circle
#from shapely.geometry import MultiPoint
#df = pd.read_csv('outputascsv_1.csv')
#coords = df.as_matrix(columns=['Longitude', 'Latitude'])
#print(len(coords))
#
#
#kms_per_radian = 6371.0088
#epsilon = 0.1 / kms_per_radian
#db = DBSCAN(eps=epsilon, min_samples=5, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
#cluster_labels = db.labels_
#num_clusters = len(set(cluster_labels))
#clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
#print('Number of clusters: {}'.format(num_clusters))
#print(clusters)
#print(clusters.shape)
#
#def get_centermost_point(cluster):
#    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
#    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
#    return tuple(centermost_point)
#centermost_points = clusters.map(get_centermost_point)
#
#lats, lons = zip(*centermost_points)
#rep_points = pd.DataFrame({'lon':lons, 'lat':lats})
#
#rs = rep_points.apply(lambda row: df[(df['lat']==row['lat']) & (df['lon']==row['lon'])].iloc[0], axis=1)
#rs.head()
##rs = rep_points.apply(lambda row: df[(df['lat']==row['lat']) and (df['lon']==row['lon'])].iloc[0], axis=1)
#

