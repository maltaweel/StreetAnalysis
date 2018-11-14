'''
Method to conduct the analysis as described in:
Porta et al. 2006. The network analysi of urban streets: a primal approach. Evironment and Planning B: Planning and Design 33:705-725.

The class conducts efficiency tests on the entire graph and also on nodes. Centrality measures are also conducted. 
Created on Nov 12, 2018

__author__: Mark Altaweel
__version__: 1.0
'''

'''
libraries to load
'''
import loadApplyModel
import networkx as nx
import math
import csv
import os
from PyQt4.QtGui import *

'''
the filename for the shapefile analyzed
'''
filename=''


def getOutuptPath(text2,fileType):
    '''The output files' path determined by the folder to plae the output and the name of the file for output.
    text2 -- the output path for the output folder
    fileType -- the file to output to the output folder
    '''
#   p=os.path.abspath(text2)
    fileN=os.path.join(text2,fileType)
    return fileN

def nodez(G):
    '''Method to return two sets of list of nodes in the graph, with both lists being the same.
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
                path = nx.shortest_path(G,weight='weight',source=n,target=n2)
                ide=math.sqrt(math.pow(n[0]-n2[0],2)+math.pow(n[1]-n2[1],2))
                ideal+=ide
                
                path_edges = zip(path,path[1:])
                actDistance=float(0)
                for e in path_edges:
                    eD=G.get_edge_data(*e)
                    actD=eD['weight']
                    actDistance+=actD
                
                glob+=float(ide/actDistance)
                    
                    
                    
                    
    print"efficiency measure: "+ str(float(glob)/(float(nx.number_of_nodes(G)*(nx.number_of_nodes(G)-1.0))))
    return float(glob)/(float(nx.number_of_nodes(G)*(nx.number_of_nodes(G)-1.0)))


def centralityMeasures(G):
    '''Method does three different centrality measures. This includes betweenness, closeness, and degree centarlity for nodes.
    G-- the graph to be analyzed
    '''
    # Betweenness centrality
    bet_cen = nx.betweenness_centrality(G)
    # Closeness centrality
    clo_cen = nx.closeness_centrality(G)
    
    # Degree centrality
    deg_cen = nx.degree_centrality(G)
    
    #print bet_cen, clo_cen, eig_cen
    print "# Betweenness centrality:" + str(bet_cen)
    print "# Closeness centrality:" + str(clo_cen)
    print "# Degree centrality:" + str(deg_cen)
    
    return bet_cen,clo_cen,deg_cen

def efficiencyCentrality(G):
    '''Method conducts efficiency centrality onn the graph.
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
                ideal+=float(1)/float(math.sqrt(math.pow(n[0]-n2[0],2)+math.pow(n[1]-n2[1],2)))
                
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
                ideal+=float(math.sqrt(math.pow(n[0]-n2[0],2)+math.pow(n[1]-n2[1],2)))
                
                path_edges = zip(path,path[1:])
                actDistance=float(0)
                for e in path_edges:
                    eD=G.get_edge_data(*e)
                    actDistance+=float(eD['weight'])
                
                glob+=actDistance
        
        value=float((ideal/glob))/float(nx.number_of_nodes(G)-1.0)
    #    print 'straightness centrality: ' +str(float((ideal/glob))/float(nx.number_of_nodes(G)-1.0))
        results[n]=value
     
       
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
        
    with open(fileN, 'wb') as csvf:
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
    loc- the folder location to print out to
    fileType-- the name of the file to print results to
    bet-- the betweenness centality results
    cent-- closeness centrality output
    degree-- degree centrality output
    '''
    fileN=getOutuptPath(loc,fileType)
     
    fieldnames = ['id','x','y','betweenness','closeness','degree']
        
    with open(fileN, 'wb') as csvf:
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


def run():
    '''
    Method to call and run the analysis.
    '''
    qid = QFileDialog()

    #fileName = "Enter the file to analyise here."
    filename = QFileDialog.getOpenFileName()


    outputFolder = "Enter the output folder location here."
    mode = QLineEdit.Normal
    #text, ok = QInputDialog.getText(qid,outputFolder,filename, mode)
    text2, ok = QInputDialog.getText(qid,filename, outputFolder, mode)
    
    G=loadApplyModel.load(filename)
    res=runGlobalEfficiency(G)
    
    bet,clos,deg=centralityMeasures(G)
    
    result1=efficiencyCentrality(G)
    result2=straightnessCentrality(G)
    
    
    printGlobalEfficiency(res,text2,'globalEfficiency.csv')
    printResults(result1,text2,"efficiencyCentrality.csv")
    printResults(result2,text2,"straightnessCentrality.csv")
    
    printNodeCentrality(text2,'nodeCentrality.csv',bet,clos,deg)
