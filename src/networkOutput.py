'''
Created on Dec 29, 2020

@author: maltaweel
'''
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication

import sys, os
import loadApplyModel
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

from networkAnalysis import NetworkAnalysis
import csv

class NetworkOutput(NetworkAnalysis):
    
    def printResults(self,results,loc,fileType):
        '''
        Method to output some of the measures results excluding global efficiency and node centrality measures.
        results-- the results to print out
        loc-- the directory location to printout the files to
        fileType-- the file to output
        '''
        fileN=self.getOutuptPath(loc,fileType)
        
        fieldnames = ['id','x','y','value']
        
        with open(fileN, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            i=0
            for ie in results:
            
                value=results[ie]
            
                writer.writerow({'id':i,'x':str(ie[0]),'y':str(ie[1]), 'value' :str(value)})
           
                i+=1

    def printNodeCentrality(self,loc,fileType,result1,result2):
        '''
        Method to print node centrality.

        loc-- the folder location to print out to
        fileType-- the name of the file to print results to
        result1-- efficiency centrality value
        result2-- straightness centrality value
        '''
        fileN=self.getOutuptPath(loc,fileType)
     
        fieldnames = ['id','x','y','betweenness','closeness','degree','efficiency',
                 'straightness','katz','eigen vector','current flow','harmonic']
        
        with open(fileN, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            i=0
            for ie in self.bet_cen.keys():
            
                value1=self.bet_cen[ie]
                value2=self.clo_cen[ie]
                value3=self.deg_cen[ie]
                value4=result1[ie]
                value5=result2[ie]
                value6=self.kcentral[ie]
                value7=self.eVector[ie]
                value8=self.cflow[ie]
                value9=self.harmonic[ie]
                #value10=self.dispersion[ie]
            
                writer.writerow({'id':i,'x':str(ie[0]),'y':str(ie[1]),
                             'betweenness':str(value1),'closeness':str(value2),
                             'degree':str(value3),'efficiency':str(value4),
                             'straightness':str(value5),'katz':str(value6),
                             'eigen vector':str(value7),'current flow':str(value8),
                             'harmonic':str(value9)})
           
                i+=1

    def printEdgeCentrality(self,loc, fileType, edges):
    
        '''Method to print betweenness centrality for edges.
         loc-- the folder location to print out to
         fileType-- the name of the file to print results to
         edges-- edges to get edge values
         '''
        
        filename=self.getOutuptPath(loc,fileType)
        
        fieldnames = ['id','x','y','value']
        
        with open(filename, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            i=0
            for ie in edges:
            
                value=edges[ie]
            
                n1=ie[0]
                n2=ie[1]
            
                n1x=n1[0]
                n1y=n1[1]
                n2x=n2[0]
                n2y=n2[1]
            
                writer.writerow({'id':i,'x':str(n1x),'y':str(n1y), 'value' :str(value)})
                writer.writerow({'id':i,'x':str(n2x),'y':str(n2y), 'value' :str(value)})
           
                i+=1

    def convertToLine(self,loc,fileType):
        data=self.getOutuptPath(loc,fileType)
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
        path_output=self.getOutuptPath(loc,'betweeness_road_data.shp')
        gdf.to_file(path_output, driver="ESRI Shapefile")   

    def centralityEdges(self,loc,fileType):
        data=self.getOutuptPath(loc,fileType)
        df = pd.read_csv(data)

        #Convert string/text/object time to datetime time
        #Create XY column
        df['XY'] = list(zip(df['x'],df['y']))


        #Group by ID. Any aggfunc is possible, python build-in or own. Also possible to have multiple funcs per field.
        aggfuncs = {'XY':list,'betweenness':'first','closeness':'first','degree':'first',
                    'katz':'first','current flow':'first','harmonic':'first','straightness':'first',
                    'efficiency':'first'}
        
        df2 = df.groupby('id').agg(aggfuncs)

        #Create geodataframe
        geometry = [LineString([Point(p) for p in row]) for row in df2['XY']]
        crs = {'init':'epsg:4326'}
        gdf = gpd.GeoDataFrame(df2, crs=crs, geometry=geometry)

        #Export to file
        gdf.reset_index(inplace=True) #To keep ID column
        del gdf['XY']
    
    #   del gdf['value']
        path_output=self.getOutuptPath(loc,'edge_centrality.shp')
        gdf.to_file(path_output, driver="ESRI Shapefile") 


    def printMultipleEdgeCentralities(self,loc, fileType, edgz, G):
       
        filename=self.getOutuptPath(loc,fileType)
        
        fieldnames = ['id','x','y','betweenness','closeness','degree','katz',
                      'current flow','harmonic','efficiency','straightness']
        
        with open(filename, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            i=0
            
            betweeness=self.bet_c
            closeness=edgz['closeness']
            degree=edgz['degree']
            katz=edgz['katz']
            cflow=edgz['current flow']
            harmonic=edgz['harmonic']
            efficiency=edgz['efficiency']
            straightness=edgz['straightness']
            
            for e in G.edges():
                bt=0
                if e in betweeness:
                    bt=betweeness[e]
                
                cv=0
                if str(e) in closeness:
                    cv=closeness[str(e)]
                
                dg=0
                if str(e) in degree:
                    dg=degree[str(e)]
                
                kz=0
                if str(e) in katz:
                    kz=katz[str(e)]
                    
                cf=0
                if str(e) in cflow:
                    cf=cflow[str(e)]
                
                hm=0
                if str(e) in harmonic:
                    hm=harmonic[str(e)]
                
                ds=0
                if str(e) in efficiency:
                    ds=efficiency[str(e)]
                    
                st=0
                if str(e) in straightness:
                    st=straightness[str(e)]

            
                n1=e[0]
                n2=e[1]
                
                n1x=n1[0]
                n1y=n1[1]
                n2x=n2[0]
                n2y=n2[1]
            
                writer.writerow({'id':i,'x':str(n1x),'y':str(n1y), 'betweenness':str(bt),'closeness':str(cv),'degree':str(dg)
                                ,'katz':str(kz),'current flow':str(cf),'harmonic':str(hm),'efficiency':str(ds),'straightness':
                str(st)})
                writer.writerow({'id':i,'x':str(n2x),'y':str(n2y), 'betweenness':str(bt),'closeness':str(cv),'degree':str(dg)
                                 ,'katz':str(kz),'current flow':str(cf),'harmonic':str(hm),'efficiency':str(ds),'straightness':
                str(st)})
           
                i+=1
                
    def run(self):
        '''
        Method to call and run the analysis.
        '''
        app = QApplication(sys.argv)
    
        qid = QFileDialog()

        #fileName = "Enter the file to analyise here."
        filename = QFileDialog.getOpenFileName()


        #outputFolder = "Enter the output folder location here."
        #mode = QLineEdit.Normal
        #text, ok = QInputDialog.getText(qid,outputFolder,filename, mode)
        # text2 = QInputDialog.getText(qid,filename[0], outputFolder, mode)
        paths=[]
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        path=os.path.join(pn,'output')
        paths.append(path)
        paths.append(pn)
        self.text2 = QInputDialog.getItem(qid,"Folder Dialog", "Select Folder", paths, 0, False)
  
        G=loadApplyModel.load(filename)
        res=self.runGlobalEfficiency(G)
    
        self.centralityMeasures(G)
    
        self.efficiencyCentrality(G)
        self.straightnessCentrality(G)
    
        #do centrality outputs to .csv files
        self.printGlobalEfficiency(res,self.text2,'globalEfficiency.csv')
        self.printResults(self.efficiency,self.text2,"efficiencyCentrality.csv")
        self.printResults(self.straightness,self.text2,"straightnessCentrality.csv")
    
        self.printNodeCentrality(self.text2,'nodeCentrality.csv',self.efficiency,self.straightness)
        self.printEdgeCentrality(self.text2,'edgeBetweenessCentrality.csv',self.bet_c)
    
        #convert betweeness edge values to .shp file
        self.convertToLine(self.text2,'edgeBetweenessCentrality.csv')
    
        edgz=self.doEdgeCentralities(G)
        self.printMultipleEdgeCentralities(self.text2,'edgeCentrality.csv',edgz, G)
        self.centralityEdges(self.text2,'edgeCentrality.csv')
            
if __name__ == '__main__':
    nt=NetworkOutput()
    nt.run()