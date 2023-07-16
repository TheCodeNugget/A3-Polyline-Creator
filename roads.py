import argparse
from pathlib import Path
import shapefile
import math
import numpy as np


def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

limiters = []
f = open("highwayMarks.txt","r")
for line in f:
    lineItems = line.split(";")
    limiters.append([float(lineItems[1]), float(lineItems[2])])
f.close()

points = []
f = open("Highway.txt","r")
for line in f:
    lineItems = line.split(";")
    points.append([float(lineItems[1]), float(lineItems[2])])
f.close()

w = shapefile.Writer("out.shp", shapeType=3)
w.field('ID', 'N')
w.field('ORDER', 'N')
        
while (len(limiters) > 1) and (len(points) > 1):
    currentLine = []
    currentPoint = limiters[0]
    limiterHold = limiters[0]
    limiters.pop(0)
    currentLine.append(currentPoint)

    while (True):
        closestLimiterIndex = closest_node(currentPoint, limiters)
        closestLimiter = limiters[closestLimiterIndex]
        closestLimiterDist = math.dist(currentPoint, closestLimiter)
        closestPointIndex = closest_node(currentPoint, points)
        closestPoint = points[closestPointIndex]
        closestPointDist = math.dist(currentPoint, closestPoint)
    
        if ((closestPointDist) > closestLimiterDist):
            break
        
        currentLine.append(closestPoint)
        currentPoint = closestPoint
        points.pop(closestPointIndex)
        
        if (len(points) == 0):
            break
    
    if (len(currentLine) == 1):
        continue
        
    currentLine.append(closestLimiter)
    #limiters.pop(closestLimiterIndex)
    limiters.append(limiterHold)
    w.line([currentLine])
    w.record(1,0)
    
    if (len(points) == 0):
        break

w.close()