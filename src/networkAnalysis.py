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
import numpy
import math
import sys
import os

class NetworkAnalysis:
    
    def getOutuptPath(self,text2,fileType):
        '''The output files' path determined by the folder to place the output and the name of the file for output.
        text2 -- the output path for the output folder
        fileType -- the file to output to the output folder
    
        fileN -- returns a file path for fileType
        '''
        #   p=os.path.abspath(text2)
        fileN=os.path.join(text2[0],fileType)
        return fileN

    def nodez(self,G):
        '''Method to return two sets of list of nodes in the graph, with both lists being the same.
        G-- the graph to be analyzed
    
        returns the following:
    
        nodes-- the first list of nodes
        nodes2-- the second list of nodes
        '''
        nodes=G.nodes
        nodes2=G.nodes
    
        return nodes, nodes2

    def runGlobalEfficiency(self,G):
        '''
        This algorithm conducts global efficiency calculations. Effectively this looks at the overall graph's efficiency
        G-- the graph analyzed
        '''
        nodes, nodes2=self.nodez(G)
    
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

    def centralityMeasures(self,G):
        '''Method does three different centrality measures. This includes betweenness, closeness, and degree centarlity for nodes.
        G-- the graph to be analyzed
        '''
        # Betweenness centrality
        self.bet_cen = nx.betweenness_centrality(G)
    
        #edge betweeness centrality
        self.bet_c=nx.edge_betweenness_centrality(G, k=None, normalized=True, weight="weight", seed=None)
    
        # Closeness centrality
        self.clo_cen = nx.closeness_centrality(G)
    
        # Degree centrality
        self.deg_cen = nx.degree_centrality(G)
    
        #Katz centrality
        self.kcentral=nx.algorithms.centrality.katz_centrality(G)
    
        #eigenvector centrality
        self.eVector=nx.algorithms.centrality.eigenvector_centrality(G,max_iter=500)
    
        #current flow centrality
        self.cflow=nx.algorithms.centrality.current_flow_closeness_centrality(G)
    
        #harmonic centrality
        self.harmonic=nx.algorithms.centrality.harmonic_centrality(G)
    
        #dispersion centarlity
#       self.dispersion=nx.algorithms.centrality.dispersion(G)
    
        #print bet_cen, clo_cen, eig_cen
        print ("Betweenness centrality:" + str(self.bet_cen))
        print ("Closeness centrality:" + str(self.clo_cen))
        print ("Degree centrality:" + str(self.deg_cen))
    

    def efficiencyCentrality(self,G):
        '''Method conducts efficiency centrality on the graph.
        G-- the graph to be analyzed
        '''
        nodes, nodes2=self.nodez(G)
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
            self.efficiency=results
       
    def straightnessCentrality(self,G):
        '''Method conducting straightness centrality.
        G-- the graph to be analyzed.
        '''
        nodes, nodes2=self.nodez(G)
    
 
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
            
            self.straightness=results
       
    
    def printGlobalEfficiency(self,res,loc,fileType):
        '''Method to print out global efficiency.
        res-- the results to print out from the graph
        loc-- the directory location to print out to
        fileType-- the file to print results on
        '''
        fileN=self.getOutuptPath(loc,fileType)
    
        f = open(fileN, "w")
        f.write("Global Efficiency: "+str(res))
    
    def doEdgeCentralities(self,G):
        centralities=[self.clo_cen,self.deg_cen,self.kcentral,self.eVector,
                      self.cflow,self.harmonic,self.efficiency,self.straightness]
        
        types=['closeness','degree','katz','eigenvector','current flow',
               'harmonic','efficiency','straightness']
        
        edgz={}
        
        for i in range(0,len(centralities)):
                       
            cent=centralities[i]
            typ=types[i]
            
            egs=G.edges()
            g=G
            
            for ed in egs:
                n1=ed[0]
                n2=ed[1]
        
                v1=cent[n1]
                v2=cent[n2]
        
                meanV=[v1,v2]
                try:
                    mean=numpy.mean(meanV)
                    
                    g[ed[0]][ed[1]]['weight']=mean
                
                except:
                    vv1=v1[n2]
                    vv2=v2[n1]
                    meanV=[vv1,vv2]
                    mean=numpy.mean(meanV)
                    
                    g[ed[0]][ed[1]]['weight']=mean

                   
            edges={}
            
            
            for ed in g.edges():
             
                try:
                    v=edges[str(ed)]
                    edges[str(ed)]=v+g[ed[0]][ed[1]]['weight']
                    
                except:
                    edges[str(ed)]=g[ed[0]][ed[1]]['weight']
       
                   
                
            edgz[typ]=edges
         
        return edgz   
