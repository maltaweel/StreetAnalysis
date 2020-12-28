'''
Method for determining closest area to betweenness locations. The application
finds the nearest polygon centre point to a road segment and then adds the value of the edge
centrality to the value for the polygon point.


Created on Nov 30, 2020

@author: maltaweel
'''
import sys
import math
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import os
import csv
import pandas as pd

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

#closeness centrality values
closeness={}

#degree centrality values
degree={}

#efficiency centrality values
efficiency={}

#straightness centrality values
straightness={}

#types of structures
types={}
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
    
    #read file and get geometry
    for i in range(0,len(zones)):
        idd=zones.id[i]
        
        #return centroid
        g = zones.geometry.centroid[i]
        
        #return the centroid betweeness value
        f = zones.value[i]
        
        xs[idd]=g
        
        values[str(g.x)+':'+str(g.y)]=f
        
    return xs, values

'''
Method that reads .csv centrality values (closeness, degree, efficiency, and straightness)
and then matches the nodes to the closest centre point values of structures.

@param xss- The polygon data for structures which have centre point data.
'''
def readOutputs(xss):
    path=getPath()
    pathway=os.path.join(path,'nodeCentrality.csv')
    
    
    with open(os.path.join(pathway),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            
           
            for row in reader:
                
                #get the .csv centrality values
                cls=row['closeness']
                dgr=row['degree']
                eff=row['efficiency']
                strr=row['straightness']
                x=row['x']
                y=row['y']
                
                distance=float('inf')
                for i in xss:
                    gg=xss[i]
                    
                    if gg is None:
                        continue
                    
                    dd=math.sqrt(math.pow((gg.x-float(x)),2.0) + math.pow((gg.y-float(y)),2.0))
                    
                    if dd<distance:
                        
                        #check to see existing value
                        if str(gg.x)+':'+str(gg.y) in closeness:
                            vv=closeness[str(gg.x)+':'+str(gg.y)]
                            if vv<cls:
                                vv=closeness[str(gg.x)+':'+str(gg.y)]
                                
                        #else apply the centrality value
                        else:
                            closeness[str(gg.x)+':'+str(gg.y)]=cls
                        
                        #same for the other centrality values as closeness 
                        if str(gg.x)+':'+str(gg.y) in degree:
                            vv=degree[str(gg.x)+':'+str(gg.y)]
                            if vv<dgr:
                                degree[str(gg.x)+':'+str(gg.y)]=dgr
                        else:   
                            degree[str(gg.x)+':'+str(gg.y)]=dgr
                        
                        if str(gg.x)+':'+str(gg.y) in efficiency:
                            vv=efficiency[str(gg.x)+':'+str(gg.y)]
                            if vv<eff:
                                efficiency[str(gg.x)+':'+str(gg.y)]=eff
                        else:   
                            efficiency[str(gg.x)+':'+str(gg.y)]=eff    
                        
                        if str(gg.x)+':'+str(gg.y) in straightness:
                            vv=straightness[str(gg.x)+':'+str(gg.y)]
                            if vv<strr:
                                straightness[str(gg.x)+':'+str(gg.y)]=strr
                        else:   
                            straightness[str(gg.x)+':'+str(gg.y)]=strr 
                            
                        distance=dd
    
   
   
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
        t= polygons.Type[i]
        
        if t is not None:
            types[str(c.x)+':'+str(c.y)]=t
       
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
        
        for idz in xss:
            gg2=xss[idz]
            
            if gg2 is None or gg is None:
                continue
            
            if gg2.x==gg.x and gg.y==gg2.y:
                continue
            
            points_df = gpd.GeoDataFrame({'geometry': [gg, gg2]}, crs='EPSG:4326')
            points_df = points_df.to_crs('EPSG:4326')
            
            #We shift the dataframe by 1 to align pnt1 with pnt2
            points_df2 = points_df.shift() 
            d=points_df.distance(points_df2)
            dd=d.array[1]
            value=vls[str(gg.x)+':'+str(gg.y)]
            
            if dd<distance:
                distance=dd
                keep[str(gg.x)+':'+str(gg.y)]=dd
                keeps.append(gg)
                twinings[str(gg.x)+':'+str(gg.y)]=gg2
                
                values[str(gg.x)+':'+str(gg.y)]=value
                
         
    return keeps, twinings, values
                
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

@param keeps- The road segment list
@param twining- The road segment associated with a polygon centre point
@param values- The assigned polygon centre values
@param xss- centre point values from polygons
'''
def doValueOutputs(keeps, twinings, values, xss):
   
    vs=[]
    
    #go through street segment center ponits and polygon centre points
    #then match best fit and value
    outs={}
    for k in keeps:
        gg2=twinings[str(k.x)+':'+str(k.y)]
    
        v=values[str(k.x)+':'+str(k.y)]
        
        if str(gg2.x)+':'+str(gg2.y) not in outs:
            outs[str(gg2.x)+':'+str(gg2.y)]=v
        else:
            vv=outs[str(gg2.x)+':'+str(gg2.y)]
            if v>vv:
                outs[str(gg2.x)+':'+str(gg2.y)]=v
        
    for i in xss:
        xs=xss[i]
        
        if xs is None:
            continue
        
        x=xs.centroid.x
        y=xs.centroid.y
        
        v=0.0
        if str(x)+':'+str(y) in outs:
            v=outs[str(x)+':'+str(y)]
        
        #input used to make shapefile
        inpt=[]
        
        try:
            cc=0.0
            dd=0.0
            ee=0.0
            ss=0.0
            tt=''
            
            #check to see if points are there for centrality values
            if str(x)+':'+str(y) in closeness:
                cc=closeness[str(x)+':'+str(y)]
            
            if str(x)+':'+str(y) in degree:
                dd=degree[str(x)+':'+str(y)]
            
            if str(x)+':'+str(y) in efficiency:
                ee=efficiency[str(x)+':'+str(y)]
            
            if str(x)+':'+str(y) in closeness:
                ss=straightness[str(x)+':'+str(y)]
                
            if str(x)+':'+str(y) in types:
                tt=types[str(x)+':'+str(y)]
        
            inpt.append(float(x))
            inpt.append(float(y))
            inpt.append(float(v))
            inpt.append(float(cc))
            inpt.append(float(dd))
            inpt.append(float(ee))
            inpt.append(float(ss))
            inpt.append(str(tt))
        
            vs.append(inpt)
        
        #handle exception
        except:
            print(str(x)+':'+str(y))
            continue
    
    #add the shapefile points (point shapefile)    
    numpy_point_array = np.array(vs)
    
    #add frame and data
    df = pd.DataFrame(numpy_point_array, columns=['X','Y','Betweeness','Closeness',
                                                  'Degree','Efficiency','Straightness','Type'])
        
    #crs and get file data to output shapfile in desired directory (in output folder)
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
    
    #do other centrality measures and assign to centroids for polygons
    readOutputs(xss)
     
    #method to find the best and nearest fits between road centres and polygon centres
    keeps, twinings, values=findBestFits(xss,xs,vals)
    
    #method to output results
    doValueOutputs(keeps, twinings, values, xss)

'''
The main to run the module.
'''    
if __name__ == '__main__':
    run()
