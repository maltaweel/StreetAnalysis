'''
Method for determining closest area to betweenness locations.


Created on Nov 30, 2020

@author: maltaweel
'''
import sys
import geopandas as gpd
import os

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
        
        values[idd]=f
        
    return xs, values
        
def loadShapeFile(shpFile):
    polygons = gpd.read_file(shpFile[0])
    
    xs={}
    
    for i in range(0,len(polygons)):
        idd=polygons.id[i]
        c= polygons.geometry.centroid[i]
       
        xs[idd]=c
    
    return xs
        
def findBestFits(xss,yss,values):   
    for idd in xss:
        gg=xss[idd]
        
        keep={}
        distance=float('inf')
        val=0.0
        
        for idz in yss:
            gg2=yss[idz]
            points_df = gpd.GeoDataFrame({'geometry': [gg, gg2]}, crs='EPSG:4326')
            points_df = points_df.to_crs('EPSG:4326')
            points_df2 = points_df.shift() #We shift the dataframe by 1 to align pnt1 with pnt2
            d=points_df.distance(points_df2)
            
            value=values[idz]
            
            if d<distance and value>val:
                distance=d
                keep[d]=gg2
    
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
    
def run():
    shpFile=os.path.join(getPath(),'path.shp')
    xs, values=readCentres(shpFile)
    
    xss=readPolygons()
    findBestFits(xss,xs,values)
    
if __name__ == '__main__':
    run()
