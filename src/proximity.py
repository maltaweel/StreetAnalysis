'''
Method for determining closest area to betweenness locations. The application
finds the nearest polygon centre point to a road segment and then adds the value of the edge
centrality to the value for the polygon point.


Created on Nov 30, 2020

@author: maltaweel
'''
import sys
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import os
import pandas as pd

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

'''
Method to get the output path
'''
def getPath():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    path=os.path.join(pn,'output')
    
    return path

'''
Method to read centre points from road segments from road path file.
''' 
def readCentres():

    app = QApplication(sys.argv)
    
    qid = QFileDialog()

    #fileName = "Enter the file to analyise here."
    filename = QFileDialog.getOpenFileName()
    
    zones = gpd.read_file(filename[0])
   
    xs={}
    values={}
    for i in range(0,len(zones)):
        idd=zones.id[i]
        
        g = zones.geometry.centroid[i]
        f = zones.value[i]
        
        xs[idd]=g
        
        values[str(g.x)+':'+str(g.y)]=f
        
    return xs, values

'''
Method to get a polygon shapefile.

@param shpFile- The polygon shapefile
'''        
def loadShapeFile(shpFile):
    #read polygons from file
    polygons = gpd.read_file(shpFile[0])
    
    xs={}
    
    for i in range(0,len(polygons)):
        idd=polygons.id[i]
        c= polygons.geometry.centroid[i]
       
        xs[idd]=c
    
    return xs

'''
Method to find the nearest point between the polygon centre and road segments.

@param xss- The polygon point centre
@param yss- The road segment points
@param vls- The values to assign to centre points for polygons
'''        
def findBestFits(xss,yss,vls):   
    keep={}
    keeps=[]
    twinings={}
    values={}
    for idd in yss:
        gg=yss[idd]
        
        distance=float('inf')
        val=0.0
        
        for idz in xss:
            gg2=xss[idz]
            
            if gg2 is None or gg is None:
                continue
            
            if gg2.x==gg.x and gg.y==gg2.y:
                continue
            
            points_df = gpd.GeoDataFrame({'geometry': [gg, gg2]}, crs='EPSG:4326')
            points_df = points_df.to_crs('EPSG:4326')
            points_df2 = points_df.shift() #We shift the dataframe by 1 to align pnt1 with pnt2
            d=points_df.distance(points_df2)
            dd=d.array[1]
            value=vls[str(gg.x)+':'+str(gg.y)]
            
            if dd<distance:
                distance=dd
                keep[str(gg.x)+':'+str(gg.y)]=dd
                keeps.append(gg)
                twinings[str(gg.x)+':'+str(gg.y)]=gg2
                
                values[str(gg.x)+':'+str(gg.y)]=value
                
    return keep, keeps, twinings, values
                
'''
Method to get and then call the readers for polygons.
'''
def readPolygons():
    
    app = QApplication(sys.argv)
    
    qid = QFileDialog()

    #fileName = "Enter the file to analyise here."
    filename = QFileDialog.getOpenFileName()

    xss=loadShapeFile(filename)
    
    return xss

'''
Output the values for polygon centre points to a shapefile.

@param keep- The road segment map
@param keeps- The road segment list
@param twining- The road segment associated with a polygon centre point
@param values- The assigned polygon centre values
'''
def doValueOutputs(keep, keeps, twinings, values):
   
    vs=[]
    
    outs={}
    for k in keeps:
        gg2=twinings[str(k.x)+':'+str(k.y)]
        d=keep[str(k.x)+':'+str(k.y)]
        v=values[str(k.x)+':'+str(k.y)]    
        if str(gg2.x)+':'+str(gg2.y) not in outs:
            outs[str(gg2.x)+':'+str(gg2.y)]=v
        else:
            vv=outs[str(gg2.x)+':'+str(gg2.y)]
            if v>vv:
                outs[str(gg2.x)+':'+str(gg2.y)]=v
        
    for xxyy in outs:
        x=xxyy.split(':')[0]
        y=xxyy.split(':')[1]
        v=outs[xxyy]
        inpt=[]
        inpt.append(float(x))
        inpt.append(float(y))
        inpt.append(float(v))
        vs.append(inpt)

        
    numpy_point_array = np.array(vs)    
    df = pd.DataFrame(numpy_point_array, columns=['X','Y','Value'])
        
    
    crs = {'init': 'EPSG:4326'}
    gdf = gpd.GeoDataFrame(
    df, crs=crs,geometry=gpd.points_from_xy(df.X, df.Y))       
    
    output=os.path.join(getPath(),'point_output.shp')
    
    gdf.to_file(driver = 'ESRI Shapefile', filename = output)

'''
Method to launch the process.
'''
def run():
   
    #method to read centre points of road data
    xs, vals=readCentres()
    
    #method to read the polygons
    xss=readPolygons()
    
    #method to find the best and nearest fits between road centres and polygon centres
    keep, keeps, twinings, values=findBestFits(xss,xs,vals)
    
    #method to output results
    doValueOutputs(keep, keeps, twinings, values)

'''
The main to run the module.
'''    
if __name__ == '__main__':
    run()