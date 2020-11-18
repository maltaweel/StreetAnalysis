'''
Method to conduct the analysis as described in:
Porta et al. 2006. The network analysis of urban streets: a primal approach. Environment and Planning B: Planning and Design 33:705-725.

The class conducts efficiency tests on the entire graph and also on nodes. Centrality measures are also conducted. 
Created on Nov 12, 2018

__author__: Mark Altaweel
__version__: 1.0
'''

'''
libraries to load
'''

import networkx as nx
import math
import csv
import os
import sys
import loadApplyModel

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

'''
the filename for the shapefile analyzed
'''
filename=''


def getOutuptPath(text2,fileType):
    '''The output files' path determined by the folder to place the output and the name of the file for output.
    text2 -- the output path for the output folder
    fileType -- the file to output to the output folder
    
    fileN -- returns a file path for fileType
    '''
#   p=os.path.abspath(text2)
    fileN=os.path.join(text2[0],fileType)
    return fileN

def nodez(G):
    '''Method to return two sets of list of nodes in the graph, with both lists being the same.
    G-- the graph to be analyzed
    
    returns the following:
    
    nodes-- the first list of nodes
    nodes2-- the second list of nodes
    '''
    nodes=G.nodes
    nodes2=G.nodes
    
    return nodes, nodes2

def runGlobalEfficiency(G):
    '''
    This algorithm conducts global efficiency calculations. Effectively this looks at the overall graph's efficiency
    G-- the graph analyzed
    '''
    nodes, nodes2=nodez(G)
    
    glob=float(0)
    ideal=float(0)
    
    for n in nodes:
        
        for n2 in nodes2:
            if n2==n:
                continue
            else:
                print(n2)
                #path = nx.shortest_path(G,weight='weight',source=n,target=n2)
                path = nx.astar_path(G, n, n2, heuristic=None, weight='weight')
                ide=math.sqrt(math.pow(math.fabs(n[0]-n2[0]),2)+math.pow(math.fabs(n[1]-n2[1]),2))
                ideal+=ide
                
                path_edges = zip(path,path[1:])
                actDistance=float(0)
                for e in path_edges:
                    eD=G.get_edge_data(*e)
                    actD=eD['weight']
                    actDistance+=actD
                
                glob+=float(ide/actDistance)
                    
        nodes2=G.nodes       
                           
    print("efficiency measure: "+ str(float(glob)/(float(nx.number_of_nodes(G)*(nx.number_of_nodes(G)-1.0)))))
    return float(glob)/(float(nx.number_of_nodes(G)*(nx.number_of_nodes(G)-1.0)))

def centralityMeasures(G):
    '''Method does three different centrality measures. This includes betweenness, closeness, and degree centarlity for nodes.
    G-- the graph to be analyzed
    '''
    # Betweenness centrality
    bet_cen = nx.betweenness_centrality(G)
    
    #edge betweeness centrality
    bet_c=nx.edge_betweenness_centrality(G, k=None, normalized=True, weight="weight", seed=None)
    
    # Closeness centrality
    clo_cen = nx.closeness_centrality(G)
    
    # Degree centrality
    deg_cen = nx.degree_centrality(G)
    
    #print bet_cen, clo_cen, eig_cen
    print ("Betweenness centrality:" + str(bet_cen))
    print ("Closeness centrality:" + str(clo_cen))
    print ("Degree centrality:" + str(deg_cen))
    
    return bet_cen,clo_cen,deg_cen, bet_c

def efficiencyCentrality(G):
    '''Method conducts efficiency centrality on the graph.
    G-- the graph to be analyzed
    '''
    nodes, nodes2=nodez(G)
    results={}
    
    for n in nodes:
        
        glob=float(0)
        ideal=float(0)
        
        for n2 in nodes2:
            if n2==n:
                continue
            else:
                path = nx.shortest_path(G,weight='weight',source=n,target=n2)
                ideal+=float(1)/float(math.sqrt(math.pow(math.fabs(n[0]-n2[0]),2)+math.pow(math.fabs(n[1]-n2[1]),2)))
                
                path_edges = zip(path,path[1:])
                actDistance=float(0)
                for e in path_edges:
                    eD=G.get_edge_data(*e)
                    actDistance+=float(1.0)/float(eD['weight'])
                
                glob+=actDistance
                
   #     print"efficiency centrality: "+ str(float(ideal/glob))
        value=float(ideal/glob)
        results[n]=value
    
    return results
    

def straightnessCentrality(G):
    '''Method conducting straightness centrality.
    G-- the graph to be analyzed.
    '''
    nodes, nodes2=nodez(G)
    
 
    results={}
    for n in nodes:
        glob=float(0)
        ideal=float(0)
        
        for n2 in nodes2:
            if n2==n:
                continue
            else:
                path = nx.shortest_path(G,weight='weight',source=n,target=n2)
                ideal+=float(math.sqrt(math.pow(math.fabs(n[0]-n2[0]),2)+math.pow(math.fabs(n[1]-n2[1]),2)))
                
                path_edges = zip(path,path[1:])
                actDistance=float(0)
                for e in path_edges:
                    eD=G.get_edge_data(*e)
                    actDistance+=float(eD['weight'])
                
                glob+=actDistance
        
        value=float((ideal/glob))/float(nx.number_of_nodes(G)-1.0)
    #    print 'straightness centrality: ' +str(float((ideal/glob))/float(nx.number_of_nodes(G)-1.0))
        results[n]=value
        nodes2=G.nodes
     
       
    return results
    
def printResults(results,loc,fileType):
    '''
    Method to output some of the measures results excluding global efficiency and node centrality measures.
    results-- the results to print out
    loc-- the directory location to printout the files to
    fileType-- the file to output
    '''
    fileN=getOutuptPath(loc,fileType)
        
    fieldnames = ['id','x','y','value']
        
    with open(fileN, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()
            
        i=0
        for ie in results:
            
            value=results[ie]
            
            writer.writerow({'id':i,'x':str(ie[0]),'y':str(ie[1]), 'value' :str(value)})
           
            i+=1
    
    
def printGlobalEfficiency(res,loc,fileType):
    '''Method to print out global efficiency.
    res-- the results to print out from the graph
    loc-- the directory location to print out to
    fileType-- the file to print results on
    '''
    fileN=getOutuptPath(loc,fileType)
    
    f = open(fileN, "w")
    f.write("Global Efficiency: "+str(res))
    
    
def printNodeCentrality(loc,fileType,bet,cent,degree):
    '''
    Method to print node centrality.
    loc-- the folder location to print out to
    fileType-- the name of the file to print results to
    bet-- the betweenness centality results
    cent-- closeness centrality output
    degree-- degree centrality output
    '''
    fileN=getOutuptPath(loc,fileType)
     
    fieldnames = ['id','x','y','betweenness','closeness','degree']
        
    with open(fileN, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()
            
        i=0
        for ie in bet.keys():
            
            value1=bet[ie]
            value2=cent[ie]
            value3=degree[ie]
            
            writer.writerow({'id':i,'x':str(ie[0]),'y':str(ie[1]),
                             'betweenness':str(value1),'closeness':str(value2),'degree':str(value3)})
           
            i+=1

def printEdgeCentrality(loc, results,fileType):
    
    '''Method to print betweenness centrality for edges.
     loc-- the folder location to print out to
    results-- the node results to convert to edges
    fileType-- the name of the file to print results to
    '''
    
    filename=getOutuptPath(loc,fileType)
        
    fieldnames = ['id','x','y','value']
        
    with open(filename, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()
            
        i=0
        for ie in results:
            
            value=results[ie]
            
            n1=ie[0]
            n2=ie[1]
            
            n1x=n1[0]
            n1y=n1[1]
            n2x=n2[0]
            n2y=n2[1]
            
            writer.writerow({'id':i,'x':str(n1x),'y':str(n1y), 'value' :str(value)})
            writer.writerow({'id':i,'x':str(n2x),'y':str(n2y), 'value' :str(value)})
           
            i+=1

def convertToLine(loc,fileType):
    data=getOutuptPath(loc,fileType)
    df = pd.read_csv(data)

    #Convert string/text/object time to datetime time
    #Create XY column
    df['XY'] = list(zip(df['x'],df['y']))

    #Group by ID. Any aggfunc is possible, python build-in or own. Also possible to have multiple funcs per field.
    aggfuncs = {'XY':list,'value':'first'}
    df2 = df.groupby('id').agg(aggfuncs)

    #Create geodataframe
    geometry = [LineString([Point(p) for p in row]) for row in df2['XY']]
    crs = {'init':'epsg:4326'}
    gdf = gpd.GeoDataFrame(df2, crs=crs, geometry=geometry)

    #Export to file
    gdf.reset_index(inplace=True) #To keep ID column
    del gdf['XY']
#   del gdf['value']
    path_output=getOutuptPath(loc,'path.shp')
    gdf.to_file(path_output, driver="ESRI Shapefile")    


def run():
    '''
    Method to call and run the analysis.
    '''
    app = QApplication(sys.argv)
    
    qid = QFileDialog()

    #fileName = "Enter the file to analyise here."
    filename = QFileDialog.getOpenFileName()


    outputFolder = "Enter the output folder location here."
    mode = QLineEdit.Normal
    #text, ok = QInputDialog.getText(qid,outputFolder,filename, mode)
    text2 = QInputDialog.getText(qid,filename[0], outputFolder, mode)
    
    G=loadApplyModel.load(filename)
    res=runGlobalEfficiency(G)
    
    bet,clos,deg, bete=centralityMeasures(G)
    
    result1=efficiencyCentrality(G)
    result2=straightnessCentrality(G)
    
    
    printGlobalEfficiency(res,text2,'globalEfficiency.csv')
    printResults(result1,text2,"efficiencyCentrality.csv")
    printResults(result2,text2,"straightnessCentrality.csv")
    
    printNodeCentrality(text2,'nodeCentrality.csv',bet,clos,deg)
    printEdgeCentrality(text2, bete,'edgeBetweenessCentrality.csv')
    
    convertToLine(text2,'edgeBetweenessCentrality.csv')

if __name__ == '__main__':
    run()