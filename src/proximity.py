'''
Method for determining closest area to betweenness locations.


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


def getPath():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    path=os.path.join(pn,'output')
    
    return path
    
def readCentres(shpFile):

    zones = gpd.read_file(shpFile)
   
    xs={}
    values={}
    for i in range(0,len(zones)):
        idd=zones.id[i]
        
        g = zones.geometry.centroid[i]
        f = zones.value[i]
        
        xs[idd]=g
        
        values[str(g.x)+':'+str(g.y)]=f
        
    return xs, values
        
def loadShapeFile(shpFile):
    polygons = gpd.read_file(shpFile[0])
    
    xs={}
    
    for i in range(0,len(polygons)):
        idd=polygons.id[i]
        c= polygons.geometry.centroid[i]
       
        xs[idd]=c
    
    return xs
        
def findBestFits(xss,yss,vls):   
    keep={}
    keeps=[]
    twinings={}
    values={}
    for idd in xss:
        gg=xss[idd]
        
        distance=float('inf')
        val=0.0
        
        for idz in yss:
            gg2=yss[idz]
            
            if gg2 is None:
                continue
            
            if gg2.x==gg.x and gg.y==gg2.y:
                continue
            
            points_df = gpd.GeoDataFrame({'geometry': [gg, gg2]}, crs='EPSG:4326')
            points_df = points_df.to_crs('EPSG:4326')
            points_df2 = points_df.shift() #We shift the dataframe by 1 to align pnt1 with pnt2
            d=points_df.distance(points_df2)
            dd=d.array[1]
            value=vls[str(gg2.x)+':'+str(gg2.y)]
            
            if dd<distance:
                distance=dd
                keep[str(gg.x)+':'+str(gg.y)]=dd
                keeps.append(gg)
                twinings[str(gg.x)+':'+str(gg.y)]=gg2
                
                values[str(gg.x)+':'+str(gg.y)]=value
                
    return keep, keeps, twinings, values
                
    
def readPolygons():
    '''
    Method to call and run the analysis.
    '''
    app = QApplication(sys.argv)
    
    qid = QFileDialog()

    #fileName = "Enter the file to analyise here."
    filename = QFileDialog.getOpenFileName()

    xss=loadShapeFile(filename)
    
    return xss

def doValueOutputs(keep, keeps, twinings, values):
   
    vs=[]
    for k in keeps:
        gg2=twinings[str(k.x)+':'+str(k.y)]
        d=keep[str(k.x)+':'+str(k.y)]
        v=values[str(k.x)+':'+str(k.y)]
        input=[]
        input.append(k.x)
        input.append(k.y)
        input.append(v)
        
        vs.append(input)

        
    numpy_point_array = np.array(vs)    
    df = pd.DataFrame(numpy_point_array, columns=['X','Y','Value'])
        
    
    crs = {'init': 'EPSG:4326'}
    gdf = gpd.GeoDataFrame(
    df, crs=crs,geometry=gpd.points_from_xy(df.X, df.Y))       
    
    gdf.to_file(driver = 'ESRI Shapefile', filename = 'point_output.shp')
    
def run():
    shpFile=os.path.join(getPath(),'path.shp')
    xs, vals=readCentres(shpFile)
    
    xss=readPolygons()
    keep, keeps, twinings, values=findBestFits(xss,xs,vals)
    
    doValueOutputs(keep, keeps, twinings, values)
    
if __name__ == '__main__':
    run()
