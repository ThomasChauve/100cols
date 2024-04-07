import pandas as pd
import datetime
import os
import numpy as np
import pickle
import streamlit as st
import plotly.express as px
import plotly.subplots

pd.set_option('display.max_rows', None)

class list100cols:

    def __init__(self,id100col=None,name=None,pseudo=None):
        self.cols=pd.DataFrame(columns=['Code', 'Nom', 'Altitude', 'Accès', 'WGS84 Lon D','WGS84 Lat D','Date'])
        self.id100col=id100col
        self.name=name
        self.pseudo=pseudo

    def save(self,adr):
        pickle.dump(self, open(adr+'.100cols','wb'))
        self.cols.to_csv(path_or_buf=adr+'.csv', sep=';')


    def add_pass(self,cols,date):
        
        idd = cols[0]
        if idd in list(self.cols.Code):
            index = list(self.cols.Code).index(idd)
            txt=list(self.cols.Nom)[index]+'('+str(list(self.cols.Altitude)[index])+')'+' a déjà été grimpé le '+str(list(self.cols.Date)[index])
            return txt
        else:
            new_pass=list(cols)
            if len(new_pass)==6: # It is very ugly I don't see the bug but it should work
                new_pass.append(date)
            elif len(new_pass)==7:
                new_pass[6]=date
                
            npdc=pd.DataFrame([new_pass],columns=['Code', 'Nom', 'Altitude', 'Accès', 'WGS84 Lon D','WGS84 Lat D','Date'])
            #st.dataframe(npdc)
            #self.cols.loc[int(ii)]=new_pass
            self.cols=pd.concat([self.cols,npdc],axis=0,ignore_index=True)
            txt=new_pass[1]+' est ajouter'
            return txt
            
    def del_pass(self,id):
        self.cols = self.cols[self.cols.Code != id]
     
        
    ### Figures ###    
    def plot_evolution_col(self):
        tt=self.cols.sort_values(by='Date')
        tt=tt.assign(nb_col = np.arange(len(tt.Date))+1)
        tt=tt.assign(nb_col2000 = np.cumsum(tt['Altitude']>=2000))
        
        fig=px.line(tt,x='Date',y=['nb_col','nb_col2000'], title='Evolution du nombre de cols')
        #fig.show()
        return fig
        
    def plot_histogram(self):
        ps=self.cols['Altitude']>=2000
        nn=[]
        for i in ps:
            if i:
                nn.append('+2000 m')
            else:
                nn.append('-2000 m')
        
        dty = [dt.year for dt in self.cols.Date.tolist()]
        bin_edges = pd.date_range(start=dty.min(), end=dty.max() + pd.Timedelta(days=365), freq='365D', closed='left')
        
        fig=px.histogram(self.cols,x='Date',pattern_shape=nn, nbins=len(bin_edges)-1, range_x=[bin_edges[0], bin_edges[-1]])
        #fig.show()
        return fig
    
    def plot_map(self,ww=1000):
        
        index=self.cols.columns

        fig = px.scatter_mapbox(self.cols, lat=index[5], lon=index[4], hover_name=index[1], hover_data=[index[0], index[2],index[6]],
                                color_discrete_sequence=["blue"], zoom=4,width=0.8*ww,height=0.3*ww)
        fig.update_layout(mapbox_style="open-street-map")
        #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    def plot_pays(self):
        pays=[]
        for i in range(len(self.cols)):
            pays.append(list(self.cols.Code)[i].split('-')[0].strip())
        a=list(set(pays))
        c=[]
        df=pd.DataFrame(columns=['Pays','Nombre de col'])
        i=0
        for n in a:
            c=pays.count(n)
            df.loc[i]=[n,c]
            i=i+1
            
        fig = px.pie(df, values="Nombre de col",names='Pays')
        return fig

    def plot_dep(self):
        dep=[]
        for i in range(len(self.cols)):
            ll=list(self.cols.Code)[i].split('-')
            #st.write(ll)
            if ll[0].strip()=='FR':
                dep.append(ll[1])
        
        a=list(set(dep))
        c=[]
        df=pd.DataFrame(columns=['Departement','Nombre de col'])
        i=0
        for n in a:
            c=dep.count(n)
            df.loc[i]=[n,c]
            i=i+1
            
        fig = px.bar(df.sort_values(by=['Departement']), x='Departement', y="Nombre de col")
        return fig
    
    
    def export_excel(self,name,idclub,datelim,out):
        tt=self.cols.copy()
        tt=tt[tt.Date>=datelim].sort_values(by='Date')
        tt.to_excel(out+'.xlsx')

    def export_pdf(self,name,idclub,datelim,out):
        # Process the pass to send
        # remove unnacessary information
        tt=self.cols.copy()
        for nn in list(tt.columns[3:6]):
            del tt[nn]

        tt=tt[tt.Date>=datelim].sort_values(by='Date')    
        # Start writing temporary markdown file
        with open(out+'_tmp.md', 'w') as f:
            f.write('![](logo.png) \n\n')
            f.write('# Mises à jour des cols \n\n')
            f.write('## Information \n\n')
            f.write('- Nom : '+name+'\n')
            f.write('- id club : '+str(idclub)+'\n')
            f.write('- Depuis : '+str(datelim)+'\n')
            f.write('- Generé le : '+str(datetime.datetime.now().date())+'\n\n')
            f.write('## Résumé \n\n')
            f.write('|         | Nombre de col |  +2000 m   |\n')
            f.write('|:-------:|:-------------:|:----------:|\n')
            f.write('|  Total  |'+str(len(self.cols))+'|'+str(np.sum(self.cols.Altitude>=2000))+'|\n')
            f.write('| Nouveau |'+str(len(tt))+'|'+str(np.sum(tt.Altitude>=2000))+'|\n\n')
            f.write('# Liste des nouveaux cols \n\n')
            f.write(tt.to_markdown())
        
        os.system('pandoc '+out+'_tmp.md -o '+out+'.pdf --pdf-engine=xelatex')
        os.system('rm '+out+'_tmp.md')

    def filter_name(self,str_r,dep=None,alt=None,date=None,print_res=True):

        id=self.cols[self.cols.columns[1]].str.contains(str_r,case=False)
        
        if alt is not None:
            id2=pd.Series(self.cols[self.cols.columns[2]]<=alt[1])
            id3=pd.Series(self.cols[self.cols.columns[2]]>=alt[0])
            id = id*id3*id2
        if date is not None:
            id2=pd.Series(self.cols[self.cols.columns[-1]]<=date[1])
            id3=pd.Series(self.cols[self.cols.columns[-1]]>=date[0])
            id = id*id3*id2
        if dep is not None:
            id2=pd.Series(self.cols[self.cols.columns[0]].str.contains(dep,case=False))
            id = id*id2
        if print_res:
            print('Nothing')
        return id
