import pandas as pd
import datetime
import os
import numpy as np
import pickle
import streamlit as st
import plotly.express as px
import plotly.subplots
import ipywidgets as widgets
from IPython.display import display, HTML

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
            ii=np.max(self.cols.index)+1
            if np.isnan(ii):
                   ii=0
            new_pass=list(cols)
            new_pass.append(date)
            self.cols.loc[int(ii)]=new_pass
            txt=self.cols.Nom.loc[ii]+'est ajouter'
            return txt
            
    def del_pass(self,id):
        self.cols=self.cols.drop(index=id)
        
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

        fig=px.histogram(self.cols,x='Date',pattern_shape=nn)
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
    
    def plot_main(self,show=False):
        fig_hist=self.plot_histogram()
        fig_cum=self.plot_evolution_col()
        fig_map=self.plot_map()
        fig_map.layout.mapbox.domain.x=(0.5,1)  
        fig_pays=self.plot_pays()
        
        fig_all=plotly.subplots.make_subplots(rows=3,cols=2,specs=[[{'type': 'xy'},{"type": 'mapbox'}],[{'type': 'xy'},None],[{'type': 'pie'},None]],shared_xaxes = True)
        
        fig_all.layout.yaxis1.title.text='Nombre'
        fig_all.layout.yaxis2.title.text='Nombre'
        fig_all.layout.xaxis2.title.text='Date'
        
        fig_all.add_trace(fig_hist.data[0],1,1)
        fig_all.add_trace(fig_hist.data[1],1,1)
        fig_all.add_trace(fig_cum.data[0],2,1)
        fig_all.add_trace(fig_cum.data[1],2,1)
        fig_all.add_trace(fig_map.data[0],1,2)
        fig_all.add_trace(fig_pays.data[0],3,1)
        fig_all.update_layout(
            fig_map.layout
        )
        fig_all.update_layout(height=800,width=1400)
        fig_all.update_layout(legend=dict(
            yanchor="bottom",
            y=0,
            xanchor="left",
            x=0
        ))
        if show:
            fig_all.show()
        else:
            return fig_all
        
    def summary(self):
    
        sort_list=['Date','Code','Altitude']
        sort=widgets.Dropdown(value=sort_list[0], options=sort_list, description='Ordre')

        ds=pd.DataFrame(columns=['Total', '+2000 m'])
        ds.loc[0]=[len(self.cols),np.sum(self.cols.Altitude>2000)]

        nb_t=widgets.Text(value=str(ds.loc[0][0]),description='Nombre:',disabled=True)
        nb_2000=widgets.Text(value=str(ds.loc[0][1]),description='+2000m:',disabled=True)

        ui=widgets.VBox([sort,widgets.HBox([nb_t,nb_2000])])

        def render_col(sort):
            tt=self.cols.sort_values(by=sort)
            display(HTML("<div style='height: 200px; overflow: auto; width: fit-content'>" +tt.style.render() +"</div>"))


        out = widgets.interactive_output(render_col,{'sort': sort})
        display(ui,out)

        return

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
            display(HTML("<div style='height: 200px; overflow: auto; width: fit-content'>" +
             self.cols.loc[np.where(id==True)[0]].style.render() +
             "</div>"))
        return id
