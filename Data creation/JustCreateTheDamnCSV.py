# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 12:30:38 2018

The idea behind this script is to have 1!! simple way
of creating a .csv file containing different routes
for the machine learning solution

@author: Viktor
"""

import RouteDuplicator, XMLToDataFrame
from pandas import DataFrame
import os

RouteDuplicator.Duplicate(5, "route_nagu.gpx")
RouteDuplicator.Duplicate(5, "route_stromso.gpx")

dataFrame = XMLToDataFrame.parse_xml(os.getcwd())
dataFrame.to_csv("DataFrame.csv")